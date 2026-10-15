import numpy as np
import rasterio

path = r".\results\Mahanadi_Susceptibility_2023_Probability.tif"

with rasterio.open(path) as src:
    p = src.read(1, masked=True).compressed()

p = p[np.isfinite(p)]

bins = [
    ("Very Low: < 0.20", 0.0, 0.20),
    ("Low: 0.20–< 0.40", 0.20, 0.40),
    ("Moderate: 0.40–< 0.60", 0.40, 0.60),
    ("High: 0.60–< 0.80", 0.60, 0.80),
    ("Very High: 0.80–1.00", 0.80, 1.000001),
]

print("Valid pixels:", len(p))
print("Minimum:", p.min())
print("Median:", np.median(p))
print("Mean:", p.mean())
print("95th percentile:", np.percentile(p, 95))
print("99th percentile:", np.percentile(p, 99))
print()

for name, lower, upper in bins:
    count = int(((p >= lower) & (p < upper)).sum())
    print(f"{name}: {count:,} pixels ({count / len(p) * 100:.3f}%)")
