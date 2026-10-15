import joblib
from pathlib import Path

model_path = Path("models/random_forest_model.pkl")
model = joblib.load(model_path)

print("Model type:", type(model).__name__)
print("Expected feature count:", model.n_features_in_)
print("Model classes:", model.classes_)
print("Number of trees:", len(model.estimators_))

if hasattr(model, "feature_names_in_"):
    print("Model feature names:", list(model.feature_names_in_))
else:
    print("Model feature names: not stored")

print("\nClass 1 probability column index:",
      list(model.classes_).index(1)
      if 1 in model.classes_ else "Class 1 not found")
