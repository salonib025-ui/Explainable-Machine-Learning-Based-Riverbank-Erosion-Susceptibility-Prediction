import os
import numpy as np
import rasterio

base = r".\results"

files = [
    "Mahanadi_Susceptibility_2023_Classes.tif",
    "Mahanadi_Susceptibility_2023_Probability.tif",
    "Mahanadi_Susceptibility_Change_2019_2023.tif",
]

for name in files:
    path = os.path.join(base, name)
    print("\n" + "=" * 65)
    print(name)

    if not os.path.exists(path):
        print("FILE NOT FOUND:", os.path.abspath(path))
        continue

    with rasterio.open(path) as ds:
        print("Dimensions:", ds.width, "x", ds.height)
        print("CRS:", ds.crs)
        print("Bounds:", ds.bounds)
        print("Pixel resolution:", ds.res)
        print("Data type:", ds.dtypes)
        print("NoData value:", ds.nodata)

        arr = ds.read(1, masked=True)
        values = arr.compressed()

        print("Valid pixels:", values.size)
        print("Missing/masked pixels:", arr.size - values.size)

        if values.size:
            print("Minimum:", float(values.min()))
            print("Maximum:", float(values.max()))
            print("Mean:", float(values.mean()))

            if "Classes" in name:
                classes, counts = np.unique(values, return_counts=True)
                print("Class counts:")
                for cls, count in zip(classes, counts):
                    print(f"  {cls}: {count:,} pixels")
