import json
from pathlib import Path

path = Path("notebooks/susceptibility_mapping.ipynb")
notebook = json.loads(path.read_text(encoding="utf-8"))

for i, cell in enumerate(notebook.get("cells", [])):
    if cell.get("cell_type") != "code":
        continue

    source = "".join(cell.get("source", []))
    if i == 9 or any(term in source.lower() for term in (
        "rf_model =",
        "joblib.load",
        "pickle.load",
        "preprocessor",
        "feature_columns",
        "feature_cols",
        "predict_proba"
    )):
        print("\n" + "=" * 75)
        print(f"CELL {i}")
        print(source)
