import cv2
import numpy as np


def extract_frames(video_path: str) -> list[np.ndarray]:
    """Extract one frame per second from a video file.

    Parameters
    ----------
    video_path : str
        Path to the input video file.

    Returns
    -------
    list[np.ndarray]
        A list of frames represented as NumPy arrays.
    """
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    fps = capture.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or np.isnan(fps):  # fallback if FPS is not available
        fps = 30
    frame_interval = max(1, int(round(fps)))

    frames = []
    frame_count = 0
    success, frame = capture.read()
    while success:
        if frame_count % frame_interval == 0:
            frames.append(frame)
        success, frame = capture.read()
        frame_count += 1

    capture.release()
    return frames

