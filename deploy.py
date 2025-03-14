import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the trained model
model = pickle.load(open("churn_xgb_optimal.pkl", "rb"))

# Define label encoding dictionaries
telecom_mapping = {"Airtel": 0, "Reliance Jio": 2, "Vodafone": 3, "BSNL": 1}
gender_mapping = {"Male": 1, "Female": 0}
state_mapping = {
    "Karnataka": 10, "Mizoram": 16, "Arunachal Pradesh": 1, "Tamil Nadu": 22, "Tripura": 24,
    "Uttarakhand": 26, "Himachal Pradesh": 8, "Rajasthan": 20, "Odisha": 18, "Uttar Pradesh": 25,
    "Chhattisgarh": 4, "Madhya Pradesh": 12, "Manipur": 14, "Goa": 5, "West Bengal": 27,
    "Gujarat": 6, "Telangana": 23, "Maharashtra": 13, "Haryana": 7, "Andhra Pradesh": 0,
    "Sikkim": 21, "Assam": 2, "Jharkhand": 9, "Kerala": 11, "Punjab": 19, "Nagaland": 17,
    "Bihar": 3, "Meghalaya": 15
}
city_mapping = {"Kolkata": 4, "Mumbai": 5, "Delhi": 2, "Chennai": 1, "Hyderabad": 3, "Bangalore": 0}

# Title and Description
st.markdown("<h1 style='text-align: center;'>Customer Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter customer details to predict churn</p>", unsafe_allow_html=True)

# User Inputs
col1, col2, col3 = st.columns(3)
gender = col1.selectbox("Gender", list(gender_mapping.keys()))
telecom_partner = col2.selectbox("Telecom Partner", list(telecom_mapping.keys()))
num_dependents = col3.number_input("Number of Dependents", min_value=0, step=1)

col4, col5 = st.columns(2)
state = col4.selectbox("State", list(state_mapping.keys()))
city = col5.selectbox("City", list(city_mapping.keys()))

col6, col7 = st.columns(2)
sms_sent = col6.number_input("SMS Sent", min_value=0, step=1)
calls_made = col7.number_input("Calls Made", min_value=0, step=1)

col8, col9 = st.columns(2)
age = col8.number_input("Age", min_value=18, step=1)
tenure_days = col9.number_input("Tenure (Days)", min_value=0, step=1)

data_used = st.number_input("Data Used (GB)", min_value=0.0, step=0.1)

# Custom styling for the Predict button
st.markdown(
    """ <style>.stButton>button { width: 200px; height: 50px; margin: 0 auto; display: block; }</style> """,
    unsafe_allow_html=True,
)

# Predict Churn
if st.button("Predict Churn"):
    # Encode categorical variables using label encoding
    gender = gender_mapping[gender]
    telecom_partner = telecom_mapping[telecom_partner]
    state = state_mapping[state]
    city = city_mapping[city]

    # Prepare input data
    data = [[gender, telecom_partner, num_dependents, state, city, sms_sent, calls_made, age, tenure_days, data_used]]
    df = pd.DataFrame(data, columns=["gender", "telecom_partner", "num_dependents", "state", "city",
                                     "sms_sent", "calls_made", "age", "tenure_days", "data_used"])

    # Predict
    single = model.predict(df)
   
    # Display Prediction
    if single == 1:
        op1 = "This Customer is likely to Churn :("
        
    else:
        op1 = "This Customer is likely to Continue!"
        
    centered_content_1 = f'<div style="text-align:center"><h3>{op1}</h3></div>'
    
    st.markdown(centered_content_1, unsafe_allow_html=True)
   