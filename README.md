# HealthRiskAI

An interactive Streamlit-based app that predicts next year's healthcare cost for patients based on their age, chronic condition score, and last year's medical cost.

## 🔍 Key Features:
- Upload batch data (CSV/Excel) of multiple patients
- Automatically select the best model for each disease:
  - OU process for mean-reverting (chronic) conditions
  - Linear regression for slow, non-reverting cases
  - Exponential for progressive, high-cost conditions
- Predict cost and flag high-risk patients
- Download result as Excel

## 📂 How it works:
- Upload a file with patient info and disease
- The model uses a reference file (`disease_model_reference.csv`) to choose prediction method
- Output includes estimated future cost and risk level

## 📥 Input Columns:
- Patient Name
- Age
- Chronic Score (0 to 1)
- Last Year Cost (USD)
- Disease Name
 
### 🚀 How to run locally:
🔗 Streamlit App:
https://healthriskaipro-dovat2hv3qp9fnhcrxtmxm.streamlit.app/


✅ Fully upgraded in July 2025.
Built with ❤️ by Safoura Yaghoubi
