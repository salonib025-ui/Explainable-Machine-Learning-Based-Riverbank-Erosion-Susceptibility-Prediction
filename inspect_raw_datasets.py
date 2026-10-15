import pandas as pd
from pathlib import Path

folder = Path("data/raw")

for path in sorted(folder.glob("Mahanadi_Erosion_*.csv")):
    print("\n" + "=" * 70)
    print("FILE:", path.name)

    df = pd.read_csv(path)

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

    if "Label" in df.columns:
        print("\nLabel distribution:")
        print(df["Label"].value_counts(dropna=False).sort_index().to_string())
