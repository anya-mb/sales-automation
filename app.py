import streamlit as st
from src.sales_automation import process

# Title of the app
st.title("Personalized Message Generator")

# Input fields
company_url = st.text_input("Company URL")
user_id = st.text_input("LinkedIn User ID")


# Dropdown menu to choose the style
style = st.selectbox("Choose message style", ["Professional", "Friendly", "Intriguing"])

additional_notes = st.text_input("Additional notes:")


# Button to generate the personalized message
if st.button("Generate personalized message"):
    if company_url and user_id:
        with st.spinner("Generating message..."):
            message = process(company_url, user_id, style, additional_notes)
            st.success(message)
    else:
        st.error("Please provide both Company URL and User ID.")
