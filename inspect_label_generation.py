import os
import json

root = "."
skip = {".git", ".venv", "venv", "__pycache__"}
terms = [
    "Mahanadi_Riverbank_Erosion_2018_2024_ML_Ready.csv",
    "to_csv(",
    "water_boundary",
    "water_change",
    "erosion_mask",
    "Feature_Year",
    "Prediction_Year",
]

for folder, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in skip]

    for filename in files:
        path = os.path.join(folder, filename)

        if filename.endswith(".py"):
            try:
                with open(path, encoding="utf-8", errors="ignore") as f:
                    source = f.read()
            except OSError:
                continue

            if any(term.lower() in source.lower() for term in terms):
                print(f"\n--- {path} ---")
                print(source[:5000])

        elif filename.endswith(".ipynb"):
            try:
                with open(path, encoding="utf-8") as f:
                    notebook = json.load(f)
            except (OSError, json.JSONDecodeError):
                continue

            for index, cell in enumerate(notebook.get("cells", [])):
                source = "".join(cell.get("source", []))

                if cell.get("cell_type") == "code" and any(
                    term.lower() in source.lower() for term in terms
                ):
                    print(f"\n--- {path} | CELL {index} ---")
                    print(source[:3500])
