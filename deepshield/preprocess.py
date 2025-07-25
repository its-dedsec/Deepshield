import cv2
import numpy as np
import mediapipe as mp


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
    """Detect and crop faces from frames."""
    mp_fd = mp.solutions.face_detection
    detector = mp_fd.FaceDetection(model_selection=0, min_detection_confidence=0.5)
    faces: list[np.ndarray] = []
    for frame in frames:
        results = detector.process(frame)
        if results.detections:
            h, w, _ = frame.shape
            for detection in results.detections:
                box = detection.location_data.relative_bounding_box
                x1 = int(max(box.xmin * w, 0))
                y1 = int(max(box.ymin * h, 0))
                x2 = int(min((box.xmin + box.width) * w, w))
                y2 = int(min((box.ymin + box.height) * h, h))
                face = frame[y1:y2, x1:x2]
                if face.size:
                    face = cv2.resize(face, (256, 256))
                    faces.append(face)
    detector.close()
    return faces

