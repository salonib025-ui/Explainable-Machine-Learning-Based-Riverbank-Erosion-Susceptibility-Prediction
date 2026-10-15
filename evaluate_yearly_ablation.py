import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"
ABLATION = ROOT / "results" / "feature_ablation"
OUTPUT = ROOT / "results" / "yearly_ablation"

raw = pd.read_csv(DATA / "Mahanadi_Riverbank_Erosion_2018_2024_ML_Ready.csv")
X_train = pd.read_csv(DATA / "X_train_processed.csv")
X_test = pd.read_csv(DATA / "X_test_processed.csv")
y_train = pd.read_csv(DATA / "y_train.csv")["Label"]
y_test = pd.read_csv(DATA / "y_test.csv")["Label"]

distance_col = "numeric__Distance_From_River"

# Verify the original temporal test split and its row order.
raw_test = raw.loc[raw["Feature_Year"] >= 2022].copy().reset_index(drop=True)
assert len(raw_test) == len(X_test) == len(y_test)
assert raw_test["Label"].equals(y_test.reset_index(drop=True)), (
    "Raw labels and processed test labels do not align."
)

# Fit fresh models with the same settings used in the ablation experiment.
feature_sets = {
    "A_All_Features": list(X_train.columns),
    "B_Without_Distance": [
        c for c in X_train.columns if c != distance_col
    ],
}

models = {}
for name, columns in feature_sets.items():
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train[columns], y_train)
    models[name] = (model, columns)

rows = []

for year in sorted(raw_test["Prediction_Year"].unique()):
    mask = raw_test["Prediction_Year"].to_numpy() == year
    actual = y_test.to_numpy()[mask]

    # A and B: Random Forest predictions on the same year-specific rows.
    for name, (model, columns) in models.items():
        X_year = X_test.loc[mask, columns]
        predicted = model.predict(X_year)
        probabilities = model.predict_proba(X_year)[:, 1]
        tn, fp, fn, tp = confusion_matrix(
            actual, predicted, labels=[0, 1]
        ).ravel()

        rows.append({
            "Prediction_Year": int(year),
            "Model": name,
            "Samples": len(actual),
            "Accuracy": accuracy_score(actual, predicted),
            "Precision": precision_score(actual, predicted, zero_division=0),
            "Recall": recall_score(actual, predicted, zero_division=0),
            "F1": f1_score(actual, predicted, zero_division=0),
            "ROC_AUC": roc_auc_score(actual, probabilities),
            "TN": tn, "FP": fp, "FN": fn, "TP": tp
        })

    # C: simple rule on original, unscaled distances.
    distance = raw_test.loc[mask, "Distance_From_River"].to_numpy()
    predicted = (distance <= 30).astype(int)
    tn, fp, fn, tp = confusion_matrix(
        actual, predicted, labels=[0, 1]
    ).ravel()

    rows.append({
        "Prediction_Year": int(year),
        "Model": "C_Distance_30m_Rule",
        "Samples": len(actual),
        "Accuracy": accuracy_score(actual, predicted),
        "Precision": precision_score(actual, predicted, zero_division=0),
        "Recall": recall_score(actual, predicted, zero_division=0),
        "F1": f1_score(actual, predicted, zero_division=0),
        "ROC_AUC": float("nan"),
        "TN": tn, "FP": fp, "FN": fn, "TP": tp
    })

OUTPUT.mkdir(parents=True, exist_ok=True)
result = pd.DataFrame(rows)
result.to_csv(OUTPUT / "yearly_metrics.csv", index=False)

print("\nYEAR-BY-YEAR TEST RESULTS")
print(result.round(4).to_string(index=False))
print(f"\nSaved to: {OUTPUT / 'yearly_metrics.csv'}")
