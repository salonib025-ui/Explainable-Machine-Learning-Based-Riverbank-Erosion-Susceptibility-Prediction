from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"
OUTPUT = ROOT / "results" / "feature_ablation"

# Load the existing preprocessed data and labels.
X_train = pd.read_csv(DATA / "X_train_processed.csv")
X_test = pd.read_csv(DATA / "X_test_processed.csv")
y_train = pd.read_csv(DATA / "y_train.csv")["Label"]
y_test = pd.read_csv(DATA / "y_test.csv")["Label"]

# Verify row counts, feature consistency, and the expected distance column.
assert len(X_train) == len(y_train), "Training rows and labels do not match."
assert len(X_test) == len(y_test), "Testing rows and labels do not match."
assert list(X_train.columns) == list(X_test.columns), (
    "Training and testing feature columns differ."
)

distance_col = "numeric__Distance_From_River"
assert distance_col in X_train.columns, (
    f"Expected column not found: {distance_col}"
)

# Compare feature groups on exactly the same train/test split.
feature_sets = {
    "A_All_Features": list(X_train.columns),
    "B_Without_Distance": [
        col for col in X_train.columns if col != distance_col
    ],
    "C_Distance_Only": [distance_col],
}

OUTPUT.mkdir(parents=True, exist_ok=True)
results = []
predictions = {}

for name, columns in feature_sets.items():
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train[columns], y_train)

    predicted = model.predict(X_test[columns])
    probabilities = model.predict_proba(X_test[columns])[:, 1]

    tn, fp, fn, tp = confusion_matrix(
        y_test, predicted, labels=[0, 1]
    ).ravel()

    metrics = {
        "Model": name,
        "Features_Count": len(columns),
        "Accuracy": accuracy_score(y_test, predicted),
        "Precision": precision_score(
            y_test, predicted, zero_division=0
        ),
        "Recall": recall_score(
            y_test, predicted, zero_division=0
        ),
        "F1": f1_score(y_test, predicted, zero_division=0),
        "ROC_AUC": roc_auc_score(y_test, probabilities),
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp,
    }
    results.append(metrics)

    predictions[name] = pd.DataFrame({
        "Actual_Label": y_test.to_numpy(),
        "Predicted_Label": predicted,
        "Probability_Class_1": probabilities,
    })

    print(f"\n{'=' * 60}")
    print(name)
    print("Features:", columns)
    print(classification_report(
        y_test, predicted, zero_division=0
    ))
    print("Confusion matrix:")
    print(np.array([[tn, fp], [fn, tp]]))

results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT / "metrics.csv", index=False)

for name, prediction_df in predictions.items():
    prediction_df.to_csv(
        OUTPUT / f"{name}_predictions.csv", index=False
    )

print(f"\n{'=' * 60}")
print("ABLATION COMPARISON")
print(results_df.round(4).to_string(index=False))
print(f"\nNew results saved to: {OUTPUT}")
print("Existing model and results were not modified.")
