import cv2
import numpy as np


def extract_frames(video_path: str, fps: int = 1) -> list[np.ndarray]:
    """Extract frames from a video at the given fps."""
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    video_fps = capture.get(cv2.CAP_PROP_FPS)
    if not video_fps or video_fps <= 0 or np.isnan(video_fps):
        video_fps = 30
    interval = max(1, int(round(video_fps / fps)))

    frames = []
    success, frame = capture.read()
    count = 0
    while success:
        if count % interval == 0:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        success, frame = capture.read()
        count += 1
    capture.release()
    return frames


def crop_faces(frames: list[np.ndarray]) -> list[np.ndarray]:
    """Detect and crop faces from frames using OpenCV's Haar cascade."""
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade_path)
    faces: list[np.ndarray] = []
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        detections = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in detections:
            face = frame[y:y + h, x:x + w]
            if face.size:
                face = cv2.resize(face, (256, 256))
                faces.append(face)
    return faces

