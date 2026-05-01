from pathlib import Path


def test_admin_can_add_new_disease_and_classifier_updates(client, admin_headers, configure_ml, temp_train_dir, encoder_path, monkeypatch):
    """
    Simulate admin adding a new disease class by uploading a couple images.
    Expectation:
    - endpoint succeeds
    - MLService recomputes prototypes + threshold
    - new class appears in ml_service.class_names
    - predicting on one of the uploaded images returns the new class (not UNKNOWN)
    """
    # Ensure service is using the temp train dir
    monkeypatch.setenv("ENCODER_PATH", encoder_path)
    monkeypatch.setenv("TRAIN_DATA_DIR", str(temp_train_dir))
    from backend.config import settings
    settings.ENCODER_PATH = encoder_path
    settings.TRAIN_DATA_DIR = str(temp_train_dir)

    # Pick 2 images from a different class (not present in temp_train_dir),
    # and upload them under a new label.
    repo_train = Path(__file__).resolve().parents[1] / "data" / "fewshot" / "train"
    src_cls = repo_train / "Tomato_Healthy"
    imgs = sorted(list(src_cls.glob("*.JPG")) + list(src_cls.glob("*.jpg")))[:2]
    assert len(imgs) >= 2, f"Expected images in {src_cls}"

    files = []
    for p in imgs:
        files.append(("files", (p.name, p.read_bytes(), "image/jpeg")))

    new_label = "New_Test_Disease"
    formatted_label = "New Test Disease"

    r = client.post(
        "/api/v1/admin/train",
        headers=admin_headers,
        data={"disease_name": new_label},
        files=files,
    )
    assert r.status_code == 200, r.text

    # Verify new class directory exists
    assert (temp_train_dir / new_label).exists()

    # Verify ml_service updated
    from backend.ml_service import ml_service
    assert formatted_label in ml_service.class_names
    assert ml_service.threshold is not None

    # Predict on one of the uploaded images
    test_img = temp_train_dir / new_label / imgs[0].name
    pred, score = ml_service.classifier.predict(str(test_img), ml_service.threshold)
    assert pred == formatted_label
    assert pred != "UNKNOWN"

