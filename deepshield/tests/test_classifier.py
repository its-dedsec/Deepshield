from deepshield.classifier import classify_faces
from deepshield.load_model import DummyModel


def test_classify_faces_dummy():
    faces = [[0], [255]]
    preds = classify_faces(faces, DummyModel())
    assert len(preds) == 2
    assert preds[0] < preds[1]

