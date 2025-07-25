from __future__ import annotations

import os
import tempfile
from datetime import datetime

import streamlit as st

from . import preprocess, load_model, classifier, report_generator, encryptor

st.set_page_config(page_title="DeepShield", layout="centered")
st.title("DeepShield Deepfake Detector")

uploaded = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])
if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.getbuffer())
        temp_path = tmp.name

    st.info("Extracting frames...")
    frames = preprocess.extract_frames(temp_path)
    progress = st.progress(0.0)
    faces = []
    for i, frame in enumerate(frames):
        faces.extend(preprocess.crop_faces([frame]))
        progress.progress((i + 1) / len(frames))
    progress.empty()

    if not faces:
        st.error("No faces detected in the video.")
    else:
        model = load_model.load_model()
        predictions = classifier.classify_faces(faces, model)
        for face, pred in zip(faces, predictions):
            st.image(face, caption=f"Score: {pred:.2f}", width=128)
        avg = sum(predictions) / len(predictions)
        decision = "DEEPFAKE" if avg >= 0.5 else "REAL"
        st.header(decision)

        report_path = report_generator.generate_report(faces, predictions, uploaded.name, decision)
        st.image(report_path, caption="Report")
        with open(report_path, "rb") as f:
            st.download_button("Download report", f, file_name="report.png")

        log_entry = f"{uploaded.name},{datetime.utcnow().isoformat()},{avg:.3f},{decision}"
        encryptor.encrypt_and_log(log_entry)
        st.success("Encrypted log saved.")

        os.remove(report_path)
    os.remove(temp_path)

