import streamlit as st
import requests
from src.rottenbot_frontend.config import Config


def predict_page():
    st.header(f"Hi {st.session_state.user_data['first_name']}!")

    # Logout button
    if st.button("Logout"):
        try:
            response = requests.get(
                Config.LOGOUT_ENDPOINT,
                headers={"Authorization": f"Bearer {st.session_state.access_token}"},
            )
            if response.status_code == 200:
                st.success("Logged out successfully.")
                st.session_state.logged_in = False
                st.session_state.user_data = None
                st.session_state.access_token = None
                st.session_state.refresh_token = None
                st.session_state.page = "main"
                st.rerun()
            else:
                st.rerun()
        except Exception as e:
            st.error(f"Logout failed: {e}")
            st.rerun()

    # image uploader
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    # let the user decide if predictions should be saved
    save_predictions = st.checkbox("Save Predictions", value=True)

    # prediction button
    if st.button("Predict"):
        if uploaded_file is not None:
            try:
                st.image(uploaded_file, caption="Uploaded Image")
                file_bytes = uploaded_file.getvalue()

                files = {"file": (uploaded_file.name, file_bytes, uploaded_file.type)}

                headers = {"Authorization": f"Bearer {st.session_state.access_token}"}

                response = requests.post(
                    f"{Config.PREDICT_ENDPOINT}?save_prediction={save_predictions}&user_uid={st.session_state.user_data['uid']}",
                    files=files,
                    headers=headers,
                )

                if response.status_code == 401:
                    st.error("Not authenticated. Please log in again.")
                    st.session_state.logged_in = False
                    st.session_state.access_token = None
                    st.session_state.refresh_token = None
                    st.rerun()
                    return

                if response.status_code == 200:
                    json_response = response.json()
                    if json_response["confidence"] < 0.9:
                        st.error(
                            f"Cannot confidently classify the image. Please use another image."
                        )
                    else:
                        st.success(
                            f"Prediction: {json_response['predicted_class_name']}"
                        )
                else:
                    st.error(f"Request failed: {response.status_code}")

            except Exception as e:
                st.error(f"Prediction failed: {e}")
        else:
            st.error("Please upload an image first.")
