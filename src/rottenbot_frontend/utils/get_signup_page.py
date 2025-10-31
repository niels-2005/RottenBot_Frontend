import streamlit as st
import requests
from src.rottenbot_frontend.config import Config


def signup_page():
    st.header("Sign Up")
    with st.form("signup_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign Up")
        if submitted:
            # HTTP request
            try:
                response = requests.post(
                    Config.SIGNUP_ENDPOINT,
                    json={
                        "user_data": {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "password": password,
                        }
                    },
                )
                data = response.json()
                st.session_state.signup_response = data
                if response.status_code == 201:
                    st.success("Sign Up successful! Redirecting to Login...")
                    st.session_state.page = "login"
                    st.rerun()
                elif (
                    response.status_code == 403
                    and data.get("detail") == "User with email already exists."
                ):
                    st.error(
                        "User with this email already exists. Please try logging in."
                    )
                else:
                    st.error(f"Sign Up failed: {response.status_code} - {data}")
            except Exception as e:
                st.error(f"Sign Up failed: {e}")

    if st.button("Already have an account? Go to Login"):
        st.session_state.page = "login"
        st.rerun()
