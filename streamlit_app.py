import os
import numpy as np
import streamlit as st
from cryptography.fernet import Fernet

from frame_classifier import classify_frames
from video_utils import extract_frames


def _simple_model(frame: np.ndarray) -> bool:
    """Dummy model classifying frames by average brightness."""
    return np.mean(frame) > 127


def _load_key(path: str = "secret.key") -> bytes:
    """Load or create an encryption key."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(path, "wb") as f:
        f.write(key)
    return key


def log_result(result: str, key_path: str = "secret.key", log_path: str = "log.txt") -> None:
    """Encrypt and log the classification result."""
    key = _load_key(key_path)
    fernet = Fernet(key)
    with open(log_path, "ab") as f:
        f.write(fernet.encrypt(result.encode()) + b"\n")


st.title("DeepShield Video Analyzer")
file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])
if file is not None:
    temp_path = "uploaded_video"
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())
    with st.spinner("Analyzing..."):
        frames = extract_frames(temp_path)
        preds = classify_frames(frames, _simple_model)
        label = "Fake" if sum(preds) / len(preds) >= 0.5 else "Real"
        log_result(label)
    st.success(f"Final classification: {label}")
    st.info("Results have been securely logged.")
    os.remove(temp_path)
