import streamlit as st
import requests
from src.rottenbot_frontend.config import Config


def login_page():
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if not email or not password:
                st.error("Email and password are required.")
                return
            # HTTP request
            try:
                response = requests.post(
                    Config.LOGIN_ENDPOINT,
                    json={
                        "login_data": {
                            "email": email,
                            "password": password,
                        }
                    },
                )
                data = response.json()
                st.session_state.login_response = data
                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.user_data = data["user"]
                    st.session_state.access_token = data["access_token"]
                    st.session_state.refresh_token = data["refresh_token"]
                    st.success("Logged in successfully! Redirecting to Predict...")
                    st.session_state.page = "predict"
                    st.rerun()
                elif response.status_code == 401:
                    st.error("Invalid email or password")
                else:
                    st.error(f"Login failed: {response.status_code} - {data}")
            except Exception as e:
                st.error(f"Login failed: {e}")

    if st.button("Don't have an account? Go to Sign Up"):
        st.session_state.page = "signup"
        st.rerun()
