import streamlit as st
import laptop_predictor
import phone_predictor

def main():
    st.title("Laptop and Phone Price Predictor")

    page = st.sidebar.selectbox("Choose Predictor", ["Home", "Laptop Predictor", "Phone Predictor"])

    if page == "Home":
        st.markdown("<h2 style='text-align: center;'>Welcome to the Price Predictor</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image("laptop.jpg", caption="Laptop Predictor", use_column_width=True)
        with col2:
            st.image("phone.jpg", caption="Phone Predictor", use_column_width=True)

    elif page == "Laptop Predictor":
        laptop_predictor.run()

    elif page == "Phone Predictor":
        phone_predictor.run()

if __name__ == "__main__":
    main()
