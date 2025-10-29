import streamlit as st


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
