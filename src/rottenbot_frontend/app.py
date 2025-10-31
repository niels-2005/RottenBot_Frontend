import streamlit as st
from src.rottenbot_frontend.utils import (
    signup_page,
    login_page,
    main_page,
    predict_page,
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None
    st.session_state.page = "main"
    st.session_state.access_token = None
    st.session_state.refresh_token = None


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
