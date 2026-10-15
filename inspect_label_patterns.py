import pandas as pd
from pathlib import Path

folder = Path("data/raw")
files = sorted(folder.glob("Mahanadi_Erosion_*.csv"))

for path in files:
    df = pd.read_csv(path)

    print("\n" + "=" * 65)
    print(path.name)

    print("\nLabel counts:")
    print(df["Label"].value_counts().sort_index().to_dict())

    for feature in [
        "Distance_From_River",
        "NDVI",
        "NDWI",
        "Elevation",
        "Rainfall",
        "LandCover",
    ]:
        print(f"\n{feature} by Label:")
        print(df.groupby("Label")[feature].agg(["mean", "median"]).round(3))
