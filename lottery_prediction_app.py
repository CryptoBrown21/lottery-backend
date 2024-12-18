import streamlit as st
import requests

# Set up the Streamlit app
def main():
    st.title("Lottery Prediction App")
    st.write("Predict your next lottery hits using advanced algorithms!")

    # Input form for initial draw and date
    draw = st.text_input("Enter Initial Draw (4 digits):", "")
    date = st.date_input("Select Date:")

    # Predict button to send data to the backend
    if st.button("Predict"):
        try:
            # Replace the URL with your working backend URL
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

if __name__ == "__main__":
    main()
