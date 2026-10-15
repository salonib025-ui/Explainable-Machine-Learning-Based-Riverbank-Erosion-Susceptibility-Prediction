import json
from pathlib import Path

path = Path("notebooks/susceptibility_mapping.ipynb")
notebook = json.loads(path.read_text(encoding="utf-8"))

keywords = (
    "predict_proba", "digitize", "searchsorted", "np.where",
    "pd.cut", "threshold", "Very Low", "Very High",
    "classes", "class_labels", "rasterio.open", "Probability.tif",
    "Classes.tif"
)

for i, cell in enumerate(notebook.get("cells", [])):
    source = "".join(cell.get("source", []))
    if cell.get("cell_type") != "code":
        continue

    lines = source.splitlines()
    matching = [
        j for j, line in enumerate(lines)
        if any(word.lower() in line.lower() for word in keywords)
    ]

    if matching:
        print("\n" + "=" * 70)
        print(f"CELL {i}")
        shown = set()
        for j in matching:
            for k in range(max(0, j - 3), min(len(lines), j + 4)):
                if k not in shown:
                    print(f"{k + 1:4}: {lines[k]}")
                    shown.add(k)
            print("    ...")
