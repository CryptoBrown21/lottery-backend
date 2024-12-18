import streamlit as st
import requests

st.title("Lottery Prediction App")

# Input form
draw = st.text_input("Enter Initial Draw (4 digits):")
date = st.date_input("Select Date:")

if st.button("Predict"):
    response = requests.post(
        "https://lottery-backend-wbft.onrender.com/predict", 
        json={"initial_draw": draw, "date": date.strftime("%m-%d")}
    )
    predictions = response.json().get("predicted_hits")
    st.write(f"Predicted Hits: {predictions}")

# Fetch and display visualizations
if st.button("Generate Visualizations"):
    response = requests.get("http://127.0.0.1:5000/visualizations")
    chart_data = response.json().get("chart")
    st.image(f"data:image/png;base64,{chart_data}")
