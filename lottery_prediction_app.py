import streamlit as st
import random

# Prediction Logic
def predict_hit_enhanced(initial_draw, date, historical_data=None):
    # Step 1: Initialize Grid
    A, B, C, D = [int(d) for d in str(initial_draw)]
    
    # Step 2: Arithmetic Rules with Extended Operations
    A_plus2, A_plus5 = (A + 2) % 10, (A + 5) % 10
    B_plus2, B_plus5 = (B + 2) % 10, (B + 5) % 10
    C_plus2, C_plus5 = (C + 2) % 10, (C + 5) % 10
    D_plus2, D_plus5 = (D + 2) % 10, (D + 5) % 10

    # Weighted Center Calculation
    Center = round((A + B + C + D) / 4) % 10
    Center_plus1 = (Center + 1) % 10
    Center_plus2 = (Center_plus1 + 1) % 10

    # Step 3: Date Sum and Mirror
    month, day = [int(d) for d in date.split('-')]
    date_sum = (month + day) % 10
    mirror_map = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
    mirror = mirror_map[date_sum]
    
    # Step 4: Circle Key Numbers
    circled_numbers = [date_sum, mirror]

    # Step 5: Prediction Grid with Additional Rules
    prediction_grid = [
        [A_plus2, mirror, B_plus2],
        [date_sum, Center_plus1, Center_plus2],
        [C_plus2, date_sum, D_plus2]
    ]
    
    # Step 6: Predicted Hits with Weights
    predicted_hits = []
    for row in prediction_grid:
        for num in row:
            if num in circled_numbers:
                predicted_hits.append((num, 2))  # Higher weight for circled numbers
            else:
                predicted_hits.append((num, 1))  # Default weight
    
    # Step 7: Historical Validation (if available)
    if historical_data:
        # Example: Use random selection for demonstration purposes
        predicted_hits = sorted(predicted_hits, key=lambda x: random.random())
    
    return {
        "grid": prediction_grid,
        "predicted_hits": [num for num, weight in predicted_hits if weight > 1]
    }

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
