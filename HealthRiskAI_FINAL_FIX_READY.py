
import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="HealthRiskAI", layout="centered")

# ------------------------- Model Definition -------------------------

def simulate_ou_process(chronic_score, last_year_cost, theta=0.5):
    mu_base = 800 + chronic_score * 1000
    sigma = 150 + chronic_score * 100
    years = np.arange(0, 11)
    x = np.zeros(len(years))
    x[0] = last_year_cost
for t in range(1, len(years)):
    predicted_cost = x[1]
    risk_score = (predicted_cost - mu_base) / sigma
    risk_level = "High" if risk_score > 0.5 else "Moderate" if risk_score > 0 else "Low"
    return round(predicted_cost, 2), round(risk_score, 2), risk_level

# ------------------------- Title -------------------------

st.title("📊 HealthRiskAI – Health Cost Forecasting Dashboard")
st.markdown("This app predicts individual healthcare costs and risk levels using the Ornstein–Uhlenbeck process.")

# ------------------------- Manual Entry -------------------------

st.header("👤 Single Patient Prediction")
age = st.slider("Age", 18, 90, 40)
chronic_score = st.slider("Chronic Condition Score (0 = Healthy, 1 = Severe)", 0.0, 1.0, 0.3, 0.05)
last_year_cost = st.number_input("Last Year's Health Cost (USD)", min_value=100, max_value=5000, value=1000)

if st.button("🔍 Predict for This Patient"):
    predicted_cost, risk_score, risk_level = simulate_ou_process(chronic_score, last_year_cost)
    st.success(f"📅 Predicted Cost for Next Year: **${{predicted_cost:.2f}}**")
    st.info(f"⚠️ Risk Score: **{{risk_score:.2f}}** → **{{risk_level}} Risk**")

# ------------------------- Batch Upload -------------------------

st.header("📥 Batch Prediction for Multiple Patients")
uploaded_file = st.file_uploader("Upload a CSV or Excel file with columns: Name, Age, Chronic_Score, Last_Year_Cost", type=["csv", "xlsx"])

if uploaded_file is not None:
     ext = os.path.splitext(uploaded_file.name)[1]
     if ext == ".csv":
     df = pd.read_csv(uploaded_file)
     elif ext == ".xlsx":
     df = pd.read_excel(uploaded_file)
     else:
     st.error("Unsupported file format!")
     st.stop()
     
     st.subheader("🔍 Uploaded Patient Data")
     st.dataframe(df)
     
     
     # بارگذاری فایل مرجع مدل بیماری‌ها
     model_ref = pd.read_csv("disease_model_reference.csv")
     
     # تابع تشخیص مدل پیشنهادی برای هر بیماری
     def get_model_for_disease(disease_name):
     row = model_ref[model_ref['Disease Name'].str.lower() == disease_name.lower()]
     if not row.empty:
     return row.iloc[0]['Suggested Model']
     else:
     return "Unknown"
     
     results = []
for _, row in df.iterrows():
    predicted_cost, risk_score, risk_level = simulate_ou_process(
    row["Chronic_Score"], row["Last_Year_Cost"]
    )
    results.append({
    "Name": row["Name"],
    "Predicted Cost (USD)": predicted_cost,
    "Risk Score": risk_score,
    "Risk Level": risk_level
    })

    results_df = pd.DataFrame(results)
    st.subheader("📈 Risk Prediction Results")
    st.dataframe(results_df)

    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", data=csv, file_name="HealthRiskAI_Results.csv", mime="text/csv")

# ------------------------- Footer -------------------------

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("---")
st.markdown("Made with ❤️ by [Safoura Yaghoubi](https://www.linkedin.com/in/safoura-yaghoubi-87bab1224) · [GitHub](https://github.com/yasamin1985)")
