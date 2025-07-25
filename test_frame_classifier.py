from frame_classifier import classify_frames


class DummyModel:
    def predict(self, frame):
        # Pretend frames are numeric scores where higher means more likely fake
        return frame


def test_classify_frames():
    frames = [0.2, 0.8, 0, 1, True, False]
    preds = classify_frames(frames, DummyModel())
    assert preds == [0, 1, 0, 1, 1, 0]
