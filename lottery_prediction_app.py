import streamlit as st
import requests

def main():
st.title("Lottery Prediction App")
st.write("Predict your next lottery hits using advanced algorithms!")
st.title("Lottery Prediction App")

# Input form for initial draw and date
draw = st.text_input("Enter Initial Draw (4 digits):", "")
date = st.date_input("Select Date:")

# Predict button to send data to the backend
if st.button("Predict"):
    try:
        response = requests.post(
            "https://lottery-backend-wbft.onrender.com/predict",  
            json={"initial_draw": draw, "date": date.strftime("%m-%d")}
        )
        if response.status_code == 200:
            predictions = response.json().get("predicted_hits")
            st.success(f"Predicted Hits: {predictions}")
        else:
            st.error("Error: Unable to fetch predictions. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")

# Generate visualizations button
st.write("## Visualizations")
if st.button("Generate Visualizations"):
    try:
        response = requests.get("https://your-backend-url.com/visualizations")  # Replace with your backend URL
        if response.status_code == 200:
            chart_data = response.json().get("chart")
            st.image(f"data:image/png;base64,{chart_data}", caption="Prediction Analysis")
        else:
            st.error("Error: Unable to fetch visualizations. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")
        if name == "main":
main()
