import io
import os
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


def _make_noise_image(path: Path, size=(224, 224)):
    arr = np.random.randint(0, 255, (size[1], size[0], 3), dtype=np.uint8)
    Image.fromarray(arr).save(path)


def test_threshold_is_reasonable(configure_ml):
    # Threshold should be a cosine similarity in [-1, 1], typically high for in-distribution.
    thr = configure_ml.threshold
    assert -1.0 <= thr <= 1.0
    assert thr > 0.2


def test_unknown_rejection_on_noise_image(configure_ml):
    # Create a synthetic OOD sample and ensure it is rejected as UNKNOWN.
    with tempfile.TemporaryDirectory() as td:
        img_path = Path(td) / "noise.jpg"
        _make_noise_image(img_path)
        pred, score = configure_ml.classifier.predict(str(img_path), configure_ml.threshold)
        assert pred == "UNKNOWN"
        assert score < configure_ml.threshold


def test_known_sample_not_unknown(configure_ml):
    # Use an existing training image; should not be rejected.
    train_dir = Path(os.environ["TRAIN_DATA_DIR"])
    any_img = next(train_dir.rglob("*.JPG"), None) or next(train_dir.rglob("*.jpg"))
    pred, score = configure_ml.classifier.predict(str(any_img), configure_ml.threshold)
    assert pred != "UNKNOWN"
    assert score >= configure_ml.threshold

