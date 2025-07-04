import streamlit as st

st.set_page_config(page_title="HealthRiskAI", page_icon="💊", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>HealthRiskAI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Predictive health risk and cost analytics using the Ornstein–Uhlenbeck process</p>", unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Health_icon.jpg/240px-Health_icon.jpg", width=100)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("HealthRiskAI: Health Cost Risk Predictor")

# Sidebar for user input
st.sidebar.header("Enter Patient Information")
age = st.sidebar.slider("Age", 18, 90, 40)
chronic_score = st.sidebar.slider("Chronic Condition Score (0 = Healthy, 1 = Severe)", 0.0, 1.0, 0.3, 0.05)
last_year_cost = st.sidebar.number_input("Last Year's Health Cost (USD)", min_value=100, max_value=5000, value=1000)

# OU process parameters
theta = 0.5
mu_base = 800 + chronic_score * 1000  # chronic score increases long-term mean cost
sigma = 150 + chronic_score * 100     # more chronic = more volatility
years = np.arange(0, 11)
x = np.zeros(len(years))
x[0] = last_year_cost

# Simulate OU process
for t in range(1, len(years)):
    x[t] = x[t - 1] + theta * (mu_base - x[t - 1]) + sigma * np.random.normal()

predicted_cost = x[1]
risk_score = (predicted_cost - mu_base) / sigma
risk_level = "High" if risk_score > 0.5 else "Moderate" if risk_score > 0 else "Low"

# Results
st.subheader("Prediction Results")
st.write(f"📅 Predicted Cost for Next Year: **${predicted_cost:.2f}**")
st.write(f"⚠️ Risk Score: **{risk_score:.2f}** → **{risk_level} Risk**")

# Plot the cost projection
st.subheader("10-Year Cost Projection (Simulated)")
fig, ax = plt.subplots()
ax.plot(years, x, marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Health Cost (USD)")
ax.set_title("Projected Health Cost Over Time")
st.pyplot(fig)

# Hide Streamlit elements and add footer
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
