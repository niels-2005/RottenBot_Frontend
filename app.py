import streamlit as st
import requests

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None
    st.session_state.page = "main"
    st.session_state.access_token = None
    st.session_state.refresh_token = None


def main_page():
    st.title("RottenBot Frontend Demo")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()


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
                    "http://127.0.0.1:8000/api/v1/auth/signup",
                    json={
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "password": password,
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


def login_page():
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            # HTTP request
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/auth/login",
                    json={"email": email, "password": password},
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


def predict_page():
    st.header("Predict")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if st.button("Vorhersagen"):
        if uploaded_file is not None:
            # Dummy HTTP request with file
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(
                    "https://httpbin.org/post", files={"file": uploaded_file}
                )
                st.session_state.predict_response = response.json()
                st.write("Prediction response:", st.session_state.predict_response)
            except Exception as e:
                st.error(f"Prediction failed: {e}")
        else:
            st.error("Please upload an image first.")


# Main logic
if st.session_state.logged_in:
    predict_page()
else:
    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "login":
        login_page()
