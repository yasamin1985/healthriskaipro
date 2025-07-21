
import streamlit as st
import pandas as pd
import numpy as np

def simulate_ou_process(chronic_score, last_year_cost, theta=0.15, mu_base=12200, sigma=100):
    T = 10
    dt = 1
    x = np.zeros(T)
    x[0] = last_year_cost
    mu = mu_base + chronic_score * 50
    for t in range(1, T):
        x[t] = x[t - 1] + theta * (mu - x[t - 1]) * dt + sigma * np.random.normal()
    predicted_cost = x[-1]
    risk_score = chronic_score * predicted_cost / 10000
    risk_level = "Low" if risk_score < 2 else "Medium" if risk_score < 5 else "High"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

def exponential_model(chronic_score, last_year_cost, disease_name=None):
    predicted_cost = last_year_cost * np.exp(0.012 * chronic_score)
    
        #  فقط برای Type 2 Diabetes adjustment می‌ذاریم:
    if disease_name == "Type 2 Diabetes":
        adjustment = 12800 / predicted_cost
        predicted_cost = predicted_cost_base * adjustment
    else:
        predicted_cost = predicted_cost_base
        
    risk_score = chronic_score * predicted_cost / 10000
    risk_level = "Low" if risk_score < 2 else "Medium" if risk_score < 5 else "High"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

def linear_model(chronic_score, last_year_cost):
    predicted_cost = last_year_cost + chronic_score * 100
    risk_score = chronic_score * predicted_cost / 10000
    risk_level = "Low" if risk_score < 2 else "Medium" if risk_score < 5 else "High"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level


def load_reference_table():
    url = "https://raw.githubusercontent.com/yasamin1985/healthriskaipro/main/disease_model_reference_FIXED2.csv"
    ref = pd.read_csv(url)
    return dict(zip(ref["Disease Name"], ref["Suggested Model"]))

st.title("📦 Batch Prediction for Multiple Patients")
st.markdown("Upload a CSV or Excel file with columns: Name, Age, Chronic_Score, Last_Year_Cost, Disease Name")

uploaded_file = st.file_uploader("Upload patient data", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        ref_table = load_reference_table()
        results = []
        for _, row in df.iterrows():
            disease = row["Disease Name"]
            model_name = ref_table.get(disease, "OU")
            if model_name == "Exponential":
                predicted_cost, risk_score, risk_level = exponential_model(row["Chronic_Score"], row["Last_Year_Cost"], disease_name=disease)
            elif model_name == "Linear":
                predicted_cost, risk_score, risk_level = linear_model(row["Chronic_Score"], row["Last_Year_Cost"])
            else:
                predicted_cost, risk_score, risk_level = simulate_ou_process(row["Chronic_Score"], row["Last_Year_Cost"])
            results.append({
                "Name": row["Name"],
                "Disease Name": disease,
                "Predicted Cost": predicted_cost,
                "Risk Score": risk_score,
                "Risk Level": risk_level,
                "Suggested Model": model_name
            })

        results_df = pd.DataFrame(results)
        st.write("### Prediction Results", results_df)

        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results as CSV", csv, "predictions_output.csv", "text/csv")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
