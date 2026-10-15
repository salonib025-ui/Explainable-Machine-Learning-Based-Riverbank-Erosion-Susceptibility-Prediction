
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# Paths and configuration
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

st.set_page_config(
    page_title="Mahanadi | Erosion Susceptibility",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Styling
# --------------------------------------------------

# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Overall application */
    .stApp,
    [data-testid="stAppViewContainer"] {
        background: #f3f7fb;
        color: #20364b;
    }

    [data-testid="stHeader"] {
        background: rgba(243, 247, 251, 0.92);
    }

    .block-container {
    padding: 1.8rem 2rem 2rem 2rem;
    max-width: 100%;
    width: 100%;
    }

    /* Main typography */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #42566b;
        line-height: 1.65;
    }

    h1, h2, h3, h4 {
        color: #15334b !important;
        letter-spacing: -0.35px;
    }

    h1 {
        font-weight: 750 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102b46 0%, #173d59 100%);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #f2f7fc !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #b8ccdc !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #36566f;
    }

    /* Sidebar navigation options */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.035);
        border-radius: 9px;
        padding: 7px 10px;
        margin-bottom: 5px;
        transition: background 0.2s ease;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.12);
    }

    /* Hero banner */
    .hero {
        padding: 2.1rem 2.2rem;
        border-radius: 20px;
        background: linear-gradient(120deg, #102b46 0%, #176b87 100%);
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 28px rgba(16, 43, 70, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .hero h1 {
        color: #ffffff !important;
        font-size: clamp(1.8rem, 3vw, 2.5rem);
        font-weight: 800 !important;
        margin: 0 0 0.75rem 0;
    }

    .hero p {
        color: #e2f1f8 !important;
        font-size: 1.02rem;
        max-width: 850px;
        margin: 0;
        line-height: 1.7;
    }

    /* Dashboard metric cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e0e9f1;
        border-radius: 15px;
        padding: 1rem 1.1rem;
        box-shadow: 0 4px 15px rgba(25, 55, 80, 0.045);
    }

    [data-testid="stMetricLabel"] {
        color: #5b7084 !important;
        font-size: 0.88rem;
    }

    [data-testid="stMetricValue"] {
        color: #123b5d !important;
        font-weight: 750;
    }

    /* General content containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #e0e9f1;
        border-radius: 14px;
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #e0e9f1;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Images */
    [data-testid="stImage"] img {
        border-radius: 12px;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button {
        border-radius: 9px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stDownloadButton button {
        border: 1px solid #cbdde9;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        border-color: #176b87;
        transform: translateY(-1px);
    }

    /* Select boxes */
    [data-testid="stSelectbox"] > div > div {
        border-radius: 9px;
        border-color: #d5e1eb;
    }

    /* Research limitation notice */
    .note {
        padding: 1rem 1.2rem;
        border-left: 4px solid #d89b2b;
        background: #fff8e8;
        border-radius: 8px;
        color: #594621;
        line-height: 1.7;
        margin: 1rem 0;
    }

    .note strong {
        color: #594621;
    }

    /* Footer */
    [data-testid="stBottomBlockContainer"] {
        border-top: 1px solid #e0e9f1;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
        }

        .hero {
            padding: 1.4rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Data-loading helpers
# --------------------------------------------------
@st.cache_data
def load_csv(path_string):
    return pd.read_csv(path_string)


def read_csv(filename):
    path = RESULTS / filename
    if not path.exists():
        st.warning(f"File not found: {path.relative_to(ROOT)}")
        return None

    try:
        return load_csv(str(path))
    except Exception as exc:
        st.error(f"Could not read {filename}: {exc}")
        return None


def show_image(filename, caption=None):
    path = RESULTS / filename
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(f"Image not found: results/{filename}")


def metric_value(df, column):
    if df is not None and not df.empty and column in df.columns:
        return float(df.iloc[0][column])
    return None


def display_percent(value):
    return f"{value:.2%}" if value is not None else "—"


# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------
st.sidebar.markdown("## 🌊 Mahanadi AI")
st.sidebar.caption("Riverbank erosion susceptibility")
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Susceptibility Maps",
        "Model Comparison",
        "Explainable AI",
        "Temporal Analysis",
        "Project Methodology",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Study area: Mahanadi River, Odisha")
st.sidebar.caption("Analysis period: 2018–2024")

# --------------------------------------------------
# Shared result data
# --------------------------------------------------
lr = read_csv("logistic_regression_results.csv")
rf = read_csv("random_forest_results.csv")
xgb = read_csv("xgboost_results.csv")
temporal = read_csv("temporal_susceptibility_summary_2019_2023.csv")

model_frames = []
for frame in [lr, rf, xgb]:
    if frame is not None and not frame.empty:
        model_frames.append(frame)

if model_frames:
    model_results = pd.concat(model_frames, ignore_index=True)
else:
    model_results = pd.DataFrame()

# --------------------------------------------------
# Overview
# --------------------------------------------------
if page == "Overview":
    st.markdown(
        """
        <div class="hero">
            <h1>Riverbank Erosion Susceptibility</h1>
            <p>
                An explainable machine-learning framework for exploring
                potential erosion susceptibility along the Mahanadi River
                downstream of Hirakud Dam, Odisha.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Project at a glance")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Dataset samples", "6,000")
    c2.metric("Year pairs", "6")
    c3.metric("Best saved accuracy", display_percent(
        metric_value(rf, "Accuracy")
    ))
    c4.metric("Best saved ROC-AUC", display_percent(
        metric_value(rf, "ROC_AUC")
    ))

    st.markdown("### Latest susceptibility map")
    show_image(
        "Mahanadi_Susceptibility_2023.png",
        "2023 susceptibility classification",
    )

    st.markdown(
        """
        <div class="note">
        <strong>Research limitation:</strong> Labels are derived from
        satellite-based water-boundary changes. They are proxy labels,
        not field-verified erosion observations. Model scores indicate
        agreement with these labels and should not be interpreted as
        verified real-world erosion accuracy.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Model performance")
    if not model_results.empty:
        st.dataframe(model_results, hide_index=True, use_container_width=True)

# --------------------------------------------------
# Susceptibility maps
# --------------------------------------------------
elif page == "Susceptibility Maps":
    st.title("🗺️ Susceptibility Maps")
    st.write(
        "Explore the existing yearly classification maps generated "
        "by the susceptibility-mapping workflow."
    )

    year = st.selectbox(
        "Select feature year",
        [2018, 2019, 2020, 2021, 2022, 2023],
        index=5,
    )

    show_image(
        f"Mahanadi_Susceptibility_{year}.png",
        f"Susceptibility classes for {year}",
    )

    st.markdown("### Probability raster")
    st.caption(
        "The GeoTIFF stores model probability values. "
        "The PNG above is the existing rendered classification map."
    )

    probability_path = (
        RESULTS / f"Mahanadi_Susceptibility_{year}_Probability.tif"
    )
    class_path = RESULTS / f"Mahanadi_Susceptibility_{year}_Classes.tif"

    c1, c2 = st.columns(2)
    with c1:
        if probability_path.exists():
            st.success(f"Probability GeoTIFF available for {year}")
            st.download_button(
                "Download probability GeoTIFF",
                data=probability_path.read_bytes(),
                file_name=probability_path.name,
                mime="image/tiff",
            )
        else:
            st.warning("Probability GeoTIFF is missing.")

    with c2:
        if class_path.exists():
            st.success(f"Class GeoTIFF available for {year}")
            st.download_button(
                "Download class GeoTIFF",
                data=class_path.read_bytes(),
                file_name=class_path.name,
                mime="image/tiff",
            )
        else:
            st.warning("Class GeoTIFF is missing.")

    st.markdown("### Change between 2019 and 2023")
    show_image(
        "Mahanadi_Susceptibility_Change_2019_2023.png",
        "Existing susceptibility-change visualization",
    )
    
    st.markdown("---")
    st.markdown("### Compare susceptibility across years")

    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        year_a = st.selectbox(
            "Earlier year",
            [2018, 2019, 2020, 2021, 2022],
            index=0,
            key="compare_year_a",
        )

    with compare_col2:
        year_b = st.selectbox(
            "Later year",
            [2019, 2020, 2021, 2022, 2023],
            index=4,
            key="compare_year_b",
        )

    map_col1, map_col2 = st.columns(2)

    with map_col1:
        st.markdown(f"#### {year_a} susceptibility")
        show_image(f"Mahanadi_Susceptibility_{year_a}.png")

    with map_col2:
        st.markdown(f"#### {year_b} susceptibility")
        show_image(f"Mahanadi_Susceptibility_{year_b}.png")

    st.caption(
        "These are the existing yearly maps. Differences may reflect "
        "changes in the modelled proxy susceptibility and should not "
        "be interpreted as independently confirmed erosion events."
    )


# --------------------------------------------------
# Model comparison
# --------------------------------------------------
elif page == "Model Comparison":
    st.title("📊 Model Comparison")
    st.write("Comparison based on the saved evaluation CSV files.")

    if model_results.empty:
        st.error("No model evaluation CSVs could be loaded.")
    else:
        st.dataframe(
            model_results,
            hide_index=True,
            use_container_width=True,
        )
    
        metric_columns = [
            "Accuracy",
            "Precision",
            "Recall",
            "F1_Score",
            "ROC_AUC",
        ]

        available = [
            col for col in metric_columns
            if col in model_results.columns
        ]

        if available and "Model" in model_results.columns:
            st.markdown("### Compare model performance")

            selected_metric = st.selectbox(
                "Choose evaluation metric",
                available,
                index=0,
                key="model_metric_selector",
                format_func=lambda metric: {
                    "Accuracy": "Accuracy",
                    "Precision": "Precision",
                    "Recall": "Recall",
                    "F1_Score": "F1-score",
                    "ROC_AUC": "ROC-AUC",
                }.get(metric, metric),
            )

            chart_df = model_results[
                ["Model", selected_metric]
            ].copy().set_index("Model")

            st.bar_chart(
                chart_df,
                y=selected_metric,
                y_label="Score",
                height=350,
                color="#168aad",
            )

            st.caption(
                "Scores measure agreement with satellite-derived "
                "proxy labels, not independently verified erosion events."
            )



    st.caption(
            "These are saved test-set metrics. Interpret them in the "
            "context of the satellite-derived proxy-label methodology."
        )

    st.markdown("### Feature importance")
    importance = read_csv("random_forest_feature_importance.csv")
    if importance is not None and not importance.empty:
        st.dataframe(importance, hide_index=True, use_container_width=True)
        if {"Feature", "Importance"}.issubset(importance.columns):
            st.bar_chart(importance.set_index("Feature")["Importance"])

# --------------------------------------------------
# Explainable AI
# --------------------------------------------------
elif page == "Explainable AI":
    st.title("🔎 Explainable AI")
    st.write(
        "Explore the saved SHAP explanations and feature-importance "
        "outputs from the existing Random Forest analysis."
    )

    left, right = st.columns(2)
    with left:
        st.markdown("#### SHAP summary")
        show_image("random_forest_shap_summary.png")

    with right:
        st.markdown("#### SHAP feature importance")
        show_image("random_forest_shap_feature_importance.png")

    st.markdown("### Dependence plots")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Distance from river**")
        show_image("shap_dependence_distance_from_river.png")
    with c2:
        st.markdown("**NDVI**")
        show_image("shap_dependence_ndvi.png")
    with c3:
        st.markdown("**NDWI**")
        show_image("shap_dependence_ndwi.png")

    shap_table = read_csv("random_forest_shap_feature_importance.csv")
    if shap_table is not None and not shap_table.empty:
        st.markdown("### Saved SHAP importance values")
        st.dataframe(shap_table, hide_index=True, use_container_width=True)

    st.info(
        "SHAP describes how features contribute to the fitted model's "
        "predictions. It does not establish that a feature causes erosion."
    )

# --------------------------------------------------
# Temporal analysis
# --------------------------------------------------
elif page == "Temporal Analysis":
    st.title("📈 Temporal Susceptibility Analysis")

    if temporal is not None and not temporal.empty:
        st.dataframe(
            temporal,
            hide_index=True,
            use_container_width=True,
        )

        if "Year" in temporal.columns:
            plot_df = temporal.set_index("Year")

            
            if "Mean_Probability" in plot_df.columns:
                st.markdown("### Mean predicted susceptibility")
                st.caption(
                    "Annual mean predicted probability across the mapped area."
                )

                st.line_chart(
                    plot_df[["Mean_Probability"]],
                    y_label="Mean predicted probability",
                    height=350,
                    color="#168aad",
                )

                if len(plot_df) >= 2:
                    first_value = float(
                        plot_df["Mean_Probability"].iloc[0]
                    )
                    last_value = float(
                        plot_df["Mean_Probability"].iloc[-1]
                    )
                    change = (last_value - first_value) * 100

                    col1, col2 = st.columns(2)
                    col1.metric(
                        "First year in summary",
                        f"{first_value:.2%}",
                    )
                    col2.metric(
                        "Last year in summary",
                        f"{last_value:.2%}",
                        delta=f"{change:+.2f} percentage points",
                    )


            class_columns = [
                "Very_Low_Percent",
                "Low_Percent",
                "Moderate_Percent",
                "High_Percent",
                "Very_High_Percent",
            ]
            class_columns = [
                col for col in class_columns if col in plot_df.columns
            ]

            if class_columns:
                st.markdown("### Susceptibility class distribution")
                st.line_chart(plot_df[class_columns])

    st.markdown("### Existing temporal visualizations")
    c1, c2 = st.columns(2)
    with c1:
        show_image("temporal_mean_susceptibility_2019_2023.png")
        show_image("temporal_very_high_susceptibility_2019_2023.png")
    with c2:
        show_image("temporal_susceptibility_class_distribution.png")
        show_image("susceptibility_change_distribution_2019_2023.png")

    change = read_csv("susceptibility_change_summary_2019_2023.csv")
    if change is not None and not change.empty:
        st.markdown("### Change summary")
        st.dataframe(change, hide_index=True, use_container_width=True)

# --------------------------------------------------
# Methodology
# --------------------------------------------------
elif page == "Project Methodology":
    st.title("🧭 Project Methodology")

    st.markdown(
        """
        **Study area:** Mahanadi River downstream of Hirakud Dam, Odisha.

        **Study period:** 2018–2024.

        ### Environmental predictors
        - NDVI — vegetation index
        - NDWI — water index
        - Elevation
        - Annual rainfall
        - Land-cover class
        - Distance from the current-year water boundary

        ### Target classes
        - **0 — Stable proxy class**
        - **1 — Potential erosion proxy class**

        ### Workflow
        1. Collect satellite and geospatial data.
        2. Derive environmental predictor layers.
        3. Generate proxy labels using changes in water masks.
        4. Construct and preprocess the dataset.
        5. Train and evaluate classification models.
        6. Interpret model predictions using SHAP.
        7. Generate susceptibility maps and analyze temporal patterns.

        ### Important interpretation
        The target is a remote-sensing-derived proxy. Water-boundary
        changes can also reflect seasonal water levels, reservoir
        fluctuations, or classification noise. The results should be
        validated against independent observations before being used
        as evidence of actual erosion.
        """
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption(
    "Academic research prototype • Mahanadi Riverbank Erosion "
    "Susceptibility • Predictions are not a substitute for field validation."
)
