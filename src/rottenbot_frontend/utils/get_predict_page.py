import streamlit as st
import requests
from src.rottenbot_frontend.config import Config


def predict_page():
    st.header("Predict")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    save_predictions = st.checkbox("Save Predictions", value=True)
    if st.button("Vorhersagen"):
        if uploaded_file is not None:
            try:
                st.image(uploaded_file, caption="Uploaded Image")
                file_bytes = uploaded_file.getvalue()

                files = {"file": (uploaded_file.name, file_bytes, uploaded_file.type)}

                response = requests.post(
                    f"{Config.PREDICT_ENDPOINT}?save_prediction={save_predictions}&user_uid={st.session_state.user_data['uid']}",
                    files=files,
                )
                json_response = response.json()
                if response.status_code == 200:
                    if json_response["confidence"] < 0.9:
                        st.error(
                            f"Cannot confidently classify the image. Please use another image."
                        )
                    else:
                        st.success(
                            f"Prediction: {json_response['predicted_class_name']}"
                        )

            except Exception as e:
                st.error(f"Prediction failed: {e}")
        else:
            st.error("Please upload an image first.")
