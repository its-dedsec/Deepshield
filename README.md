# DeepShield

DeepShield is a simple web application for detecting deepfakes in video files. It extracts frames from an uploaded video, detects faces, classifies them with a deepfake detection model and produces a report with screenshots.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run deepshield/app.py
```

## Features

- Upload a video through the web interface
- Faces are detected from 1 FPS frames using MediaPipe
- Each face is classified by a model (a dummy model is used if TensorFlow weights are missing)
- Results are shown with thumbnails and a final decision banner
- An image report can be downloaded
- All results are logged to an AES encrypted file

## Tests

Run tests with:

```bash
pytest
```

