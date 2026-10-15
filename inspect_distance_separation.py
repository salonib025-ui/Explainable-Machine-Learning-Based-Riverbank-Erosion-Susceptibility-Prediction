import pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score

for path in sorted(Path("data/raw").glob("Mahanadi_Erosion_*.csv")):
    df = pd.read_csv(path)

    # A smaller river distance is associated with Label 1.
    score = -df["Distance_From_River"]

    auc = roc_auc_score(df["Label"], score)

    print(f"\n{path.name}")
    print(f"Distance-only ROC-AUC: {auc:.4f}")

    for threshold in [25, 50, 100, 200, 500]:
        predicted = (df["Distance_From_River"] <= threshold).astype(int)
        accuracy = (predicted == df["Label"]).mean()
        print(f"Threshold {threshold:>3} m: accuracy = {accuracy:.3f}")
