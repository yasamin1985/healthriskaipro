
import streamlit as st
import pandas as pd
import numpy as np
import base64

# -------------------------------
# OU Simulation Function
# -------------------------------
def simulate_ou_process(chronic_score, last_year_cost, theta=0.5, mu=5000, sigma=300):
    np.random.seed(42)
    T = 1
    dt = 1
    steps = int(T / dt)
    x = np.zeros(steps)
    x[0] = last_year_cost
    for t in range(1, steps):
        x[t] = x[t - 1] + theta * (mu - x[t - 1]) * dt + sigma * np.random.normal()
    predicted_cost = x[-1]
    risk_score = chronic_score * predicted_cost / 10000
    risk_level = "High" if risk_score > 0.7 else "Low"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

# -------------------------------
# Linear Regression Simulation
# -------------------------------
def simulate_linear(chronic_score, last_year_cost):
    predicted_cost = 500 + 1.2 * last_year_cost + 300 * chronic_score
    risk_score = chronic_score * predicted_cost / 10000
    risk_level = "High" if risk_score > 0.7 else "Low"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

# -------------------------------
# Exponential Regression Simulation
# -------------------------------
def simulate_exponential(chronic_score, last_year_cost):
    predicted_cost = last_year_cost * np.exp(0.03 * chronic_score)
    risk_score = chronic_score * predicted_cost / 10000
    risk_level = "High" if risk_score > 0.7 else "Low"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

# -------------------------------
# Load Reference Table
# -------------------------------
@st.cache_data
def load_reference_table():
    ref = pd.read_csv("disease_model_reference.csv")
    return dict(zip(ref["Name"], ref["Model"]))

# -------------------------------
# App UI
# -------------------------------
st.set_page_config(page_title="Health Risk AI", layout="centered")
st.title("📊 Batch Prediction for Multiple Patients")
st.markdown("Upload a CSV or Excel file with columns: Name, Age, Chronic_Score, Last_Year_Cost")

uploaded_file = st.file_uploader("Drag and drop file here", type=["csv", "xlsx"])

# -------------------------------
# Process File
# -------------------------------
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except:
        st.error("❌ File format is not correct.")
        st.stop()

    ref_table = load_reference_table()

    results = []
    for _, row in df.iterrows():
        name = row["Name"]
        chronic_score = row["Chronic_Score"]
        last_year_cost = row["Last_Year_Cost"]
        model = ref_table.get(name, "Linear")

        if model == "OU":
            pred, score, level = simulate_ou_process(chronic_score, last_year_cost)
        elif model == "Exponential":
            pred, score, level = simulate_exponential(chronic_score, last_year_cost)
        else:
            pred, score, level = simulate_linear(chronic_score, last_year_cost)

        results.append({
            "Name": name,
            "Model Used": model,
            "Predicted Cost": pred,
            "Risk Score": score,
            "Risk Level": level
        })

    results_df = pd.DataFrame(results)
    st.success("✅ Predictions completed.")
    st.dataframe(results_df)

    # -------------------------------
    # Download Button
    # -------------------------------
    csv_data = results_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results as CSV", csv_data, file_name="predictions_output.csv", mime="text/csv")
