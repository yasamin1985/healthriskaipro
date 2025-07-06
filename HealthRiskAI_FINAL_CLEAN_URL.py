
import pandas as pd
import streamlit as st
import numpy as np

def load_reference_table():
    url = "https://raw.githubusercontent.com/yasamin1985/healthriskaipro/main/disease_model_reference_FIXED_2.csv"
    ref = pd.read_csv(url)
    return dict(zip(ref["Disease Name"], ref["Suggested Model"]))

def predict_cost(age, chronic_score, last_year_cost, model_type):
    if model_type == "Linear":
        return last_year_cost + (age * 2) + (chronic_score * 100)
    elif model_type == "Exponential":
        return last_year_cost * np.exp(0.01 * age + 0.05 * chronic_score)
    elif model_type == "OU":
        theta = 5000
        mu = 3000
        sigma = 0.1
        return mu + (last_year_cost - mu) * np.exp(-theta) + sigma * np.sqrt(1 - np.exp(-2 * theta))
    else:
        return last_year_cost

st.title("Batch Prediction for Multiple Patients")

uploaded_file = st.file_uploader("Upload patient data", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    required_columns = {"Name", "Age", "Chronic_Score", "Last_Year_Cost", "Disease Name"}
    if not required_columns.issubset(df.columns):
        st.error(f"Please upload a file with the following columns: {required_columns}")
    else:
        ref_table = load_reference_table()
        df["Suggested_Model"] = df["Disease Name"].map(ref_table)
        df["Predicted_Cost"] = df.apply(lambda row: predict_cost(
            row["Age"], row["Chronic_Score"], row["Last_Year_Cost"], row["Suggested_Model"]), axis=1)
        st.success("Prediction completed.")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Predictions", data=csv, file_name="predictions_output.csv", mime="text/csv")
