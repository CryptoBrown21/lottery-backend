import streamlit as st
import random

# Streamlit App
def main():
    st.title("Lottery Prediction App")
    st.write("Predict your next lottery hits using advanced algorithms!")

    # Input form for initial draw and date
    draw = st.text_input("Enter Initial Draw (4 digits):", "")
    date = st.date_input("Select Date:")

    if st.button("Predict"):
        try:
            if not draw.isdigit() or len(draw) != 4:
                st.error("Initial draw must be a 4-digit number.")
            else:
                # Call the prediction function
                date_str = date.strftime("%m-%d")
                result = predict_hit_enhanced(draw, date_str)
                st.success(f"Predicted Hits: {result['predicted_hits']}")
                st.write("Prediction Grid:")
                st.write(result["grid"])
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
