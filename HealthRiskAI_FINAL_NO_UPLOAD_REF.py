
import streamlit as st
import pandas as pd
import numpy as np

# Load disease model reference from GitHub
@st.cache_data
def load_reference_table():
    url = "https://raw.githubusercontent.com/yasamin1985/healthriskaipro/main/disease_model_reference_FIXED.csv"
    ref = pd.read_csv(url)
    return dict(zip(ref["Disease Name"], ref["Suggested Model"]))

def simulate_ou_process(chronic_score, last_year_cost, theta=0.5, mu_base=1.0, sigma=0.1, T=10):
    dt = 1
    mu = mu_base + chronic_score
    x = [np.log(last_year_cost + 1)]
    for t in range(1, T):
        x.append(x[t - 1] + theta * (mu - x[t - 1]) + sigma * np.random.normal())
    predicted_cost = np.exp(x[-1]) - 1
    risk_score = chronic_score * (predicted_cost / 10000)
    risk_level = "High" if risk_score > 1.5 else "Medium" if risk_score > 0.7 else "Low"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

def linear_model(age, chronic_score, last_year_cost):
    predicted_cost = last_year_cost + (age * 2) + (chronic_score * 100)
    risk_score = chronic_score * 0.5
    risk_level = "High" if risk_score > 1.5 else "Medium" if risk_score > 0.7 else "Low"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

def exponential_model(age, chronic_score, last_year_cost):
    predicted_cost = last_year_cost * np.exp(0.05 * age + 0.1 * chronic_score)
    risk_score = chronic_score * (predicted_cost / 15000)
    risk_level = "High" if risk_score > 2.0 else "Medium" if risk_score > 1.0 else "Low"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

model_functions = {
    "OU": simulate_ou_process,
    "Linear": linear_model,
    "Exponential": exponential_model
}

# App title
st.title("📦 Batch Prediction for Multiple Patients")
st.write("Upload a CSV or Excel file with columns: Name, Age, Chronic_Score, Last_Year_Cost")

# Upload patient data file
uploaded_file = st.file_uploader("Upload patient data", type=["csv", "xlsx"])

# Process and predict
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        ref_table = load_reference_table()

        results = []
        for _, row in df.iterrows():
            disease = row["Name"]
            model_name = ref_table.get(disease, "OU")
            model_func = model_functions.get(model_name, simulate_ou_process)

            if model_name == "OU":
                predicted_cost, risk_score, risk_level = model_func(
                    row["Chronic_Score"], row["Last_Year_Cost"]
                )
            else:
                predicted_cost, risk_score, risk_level = model_func(
                    row["Age"], row["Chronic_Score"], row["Last_Year_Cost"]
                )

            results.append({
                "Name": disease,
                "Predicted Cost": predicted_cost,
                "Risk Score": risk_score,
                "Risk Level": risk_level
            })

        results_df = pd.DataFrame(results)
        st.subheader("🔍 Prediction Results")
        st.dataframe(results_df)

        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Predictions", csv, "predictions_output.csv", "text/csv")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
