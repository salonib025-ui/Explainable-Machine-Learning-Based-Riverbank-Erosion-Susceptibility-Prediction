# Explainable Machine Learning-Based Riverbank Erosion Susceptibility Prediction

## Overview

This project develops a machine learning-based framework for predicting potential riverbank erosion susceptibility along the Mahanadi River downstream of Hirakud Dam, Odisha.

The project uses satellite and geospatial data to derive environmental features and a remote-sensing-based erosion proxy. Machine learning models are then used to classify locations as stable or potentially susceptible to erosion.

Explainable AI techniques will be used in later stages to understand the contribution of different environmental factors to model predictions.

> **Note:** The erosion labels used in this project are remote-sensing-based proxy labels and are not field-verified erosion observations.

---

## Study Area

The study area is located along the Mahanadi River downstream of Hirakud Dam in Odisha, India.

The analysis covers the period from **2018 to 2024**.

---

## Objectives

- Generate a multi-year riverbank erosion dataset using satellite and geospatial data.
- Identify environmental factors associated with potential riverbank erosion.
- Develop machine learning models for erosion susceptibility classification.
- Compare different machine learning algorithms.
- Apply explainable AI techniques to interpret model predictions.
- Analyze temporal patterns in potential erosion susceptibility.

---

## Data Sources

The project uses the following datasets:

| Dataset | Purpose |
|---|---|
| Sentinel-2 | NDVI, NDWI and river water extraction |
| SRTM DEM | Elevation |
| CHIRPS | Annual rainfall |
| Dynamic World | Land-cover classification |

---

## Features

The machine learning dataset contains the following environmental features:

- **NDVI** – Normalized Difference Vegetation Index
- **NDWI** – Normalized Difference Water Index
- **Elevation** – Elevation from SRTM DEM
- **Rainfall** – Annual rainfall from CHIRPS
- **LandCover** – Dynamic World land-cover class
- **Distance_From_River** – Distance from the current-year river water boundary

### Target
0 → Stable
1 → Potential Erosion

The target is generated using changes in the river water boundary between consecutive years.

Latitude and longitude are retained as spatial metadata and are not used as machine learning predictors.

### Temporal Dataset

The dataset is constructed using consecutive year pairs:
2018 → 2019
2019 → 2020
2020 → 2021
2021 → 2022
2022 → 2023
2023 → 2024

The final dataset contains:
6,000 samples
3,000 Stable samples
3,000 Potential Erosion samples
6 year-pairs
No missing values
No duplicate rows

### Methodology
Study Area
     ↓
Satellite & Geospatial Data Collection
     ↓
Feature Extraction
     ↓
NDVI / NDWI / Elevation / Rainfall /
Land Cover / Distance From River
     ↓
Erosion Proxy Label Generation
     ↓
Dataset Construction
     ↓
Data Preprocessing
     ↓
Temporal Train-Test Split
     ↓
Machine Learning Models
     ↓
Model Evaluation
     ↓
Explainable AI

### Data Preprocessing
The preprocessing workflow includes:
Missing-value checking
Duplicate checking
Exploratory data analysis
Numerical feature standardization
Categorical feature encoding
Temporal train-test splitting

### Training Data
Feature years from 2018–2021 are used for training.

### Testing Data
Feature years from 2022–2023 are used for testing.

This temporal split helps evaluate the models on later years that were not used during training.

### Machine Learning Models
The project currently includes:
## Logistic Regression
Logistic Regression is implemented as the initial baseline classification model.

##Planned models include:
Random Forest
XGBoost
The models will be evaluated and compared using their actual experimental results.

### Model Evaluation
The following metrics are used for evaluating the classification models:
Accuracy
Precision
Recall
F1-score
ROC-AUC
Confusion Matrix
ROC Curve
Model comparison will be added as additional algorithms are implemented.

### Explainable AI
Explainable AI will be incorporated using SHAP (SHapley Additive exPlanations).
SHAP will be used to investigate:
Feature importance
Feature contribution to predictions
Positive and negative effects of environmental variables
Individual model predictions

### Project Structure
Mahanadi-Riverbank-Erosion-ML/
│
├── data/
│   ├── raw/
│   │   ├── Mahanadi_Erosion_2018_2019.csv
│   │   ├── Mahanadi_Erosion_2019_2020.csv
│   │   ├── Mahanadi_Erosion_2020_2021.csv
│   │   ├── Mahanadi_Erosion_2021_2022.csv
│   │   ├── Mahanadi_Erosion_2022_2023.csv
│   │   └── Mahanadi_Erosion_2023_2024.csv
│   │
│   └── processed/
│       ├── Mahanadi_Riverbank_Erosion_2018_2024_ML_Ready.csv
│       ├── processed_feature_names.csv
│       ├── X_train_processed.csv
│       ├── X_test_processed.csv
│       ├── y_train.csv
│       └── y_test.csv
│
├── models/
│   └── logistic_regression_model.pkl
│
├── notebooks/
│   ├── eda_ml_preprocessing.ipynb
│   └── logistic_regression.ipynb
│
├── results/
│   ├── logistic_regression_coefficients.csv
│   └── logistic_regression_results.csv
│
├── src/
│
├── .gitignore
└── README.md
Current Results

The first machine learning model implemented is Logistic Regression.

The trained model is stored in:
models/logistic_regression_model.pkl

The model results are stored in:
results/logistic_regression_results.csv

The feature coefficients are stored in:
results/logistic_regression_coefficients.csv

Additional models and comparative results will be added as the project progresses.

### Technologies Used
Python
Pandas
NumPy
Scikit-learn
Matplotlib
Seaborn
Joblib
Google Earth Engine
Sentinel-2
SRTM
CHIRPS
Dynamic World
SHAP

### Future Work
Implement Random Forest
Implement XGBoost
Compare machine learning models
Perform SHAP-based explainability
Perform spatial and temporal susceptibility analysis
Generate riverbank erosion susceptibility maps
Develop visualizations for model results

### Disclaimer
This project is developed for academic and research purposes.
The erosion labels represent satellite-derived potential erosion indicators and should not be considered field-verified erosion measurements. The predictions are intended to support analysis of potential susceptibility and should not replace detailed field, hydrological, or geomorphological assessments.


