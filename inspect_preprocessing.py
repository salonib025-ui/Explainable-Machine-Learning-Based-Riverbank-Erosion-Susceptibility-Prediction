import json
from pathlib import Path

path = Path("notebooks/susceptibility_mapping.ipynb")
nb = json.loads(path.read_text(encoding="utf-8"))

for i, cell in enumerate(nb.get("cells", [])):
    if cell.get("cell_type") != "code":
        continue

    source = "".join(cell.get("source", []))
    if any(term in source for term in (
        "NUMERIC_FEATURES",
        "CATEGORICAL_FEATURES",
        "scaler =",
        "encoder =",
        "MODEL_PATH",
        "predict_proba"
    )):
        print("\n" + "=" * 65)
        print(f"CELL {i}")
        print(source)
