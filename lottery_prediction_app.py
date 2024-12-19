import streamlit as st
import requests

# Set up the Streamlit app
def main():
    st.title("Lottery Analysis App")
    st.write("Analyze your lottery draws and identify patterns with advanced algorithms!")

    # Input form for initial draw and date
    draw = st.text_input("Enter Initial Draw (4 digits):", "")
    month = st.number_input("Enter Month (1-12):", min_value=1, max_value=12, step=1)
    day = st.number_input("Enter Day (1-31):", min_value=1, max_value=31, step=1)

    # Analyze button to send data to the backend
    if st.button("Analyze"):
        try:
            # Ensure the draw input is valid
            if not draw.isdigit() or len(draw) != 4:
                st.error("Initial draw must be a 4-digit number.")
                return

            # Replace the URL with your working backend URL
            backend_url = "https://lottery-backend-wbft.onrender.com/analyze"

            # Prepare the request payload
            payload = {
                "previous_draw": int(draw),
                "month": int(month),
                "day": int(day)
            }

            # Send POST request to the backend
            response = requests.post(backend_url, json=payload)

            if response.status_code == 200:
                result = response.json()

                # Display the analysis results
                st.success("Analysis Successful!")

                st.write("### Generated Grid:")
                grid = result.get("grid", [])
                for row in grid:
                    st.write(row)

                st.write(f"### Date Sum: {result.get('date_sum')}")

                patterns = result.get("patterns", [])
                if patterns:
                    st.write("### Identified Patterns:")
                    for pattern in patterns:
                        st.write(pattern)
                else:
                    st.write("No patterns identified.")

            else:
                st.error(f"Error: Unable to fetch analysis. Backend responded with status {response.status_code}.")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
