import os
import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import get_db
from backend.models import Base
from backend.ml_service import ml_service


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def encoder_path() -> str:
    p = PROJECT_ROOT / "backend" / "ml" / "encoder_supcon.pth"
    assert p.exists(), f"Missing encoder weights at {p}"
    return str(p)


@pytest.fixture()
def temp_train_dir() -> Path:
    """
    Create a tiny ImageFolder-style train dir with 2 known classes,
    copied from the repo's data/fewshot/train to keep inference realistic
    and avoid changing model weights/metrics.
    """
    src_root = PROJECT_ROOT / "data" / "fewshot" / "train"
    assert src_root.exists(), f"Missing train data at {src_root}"

    tmp = Path(tempfile.mkdtemp(prefix="agroai_train_"))
    # Start with a single known class to make "add new disease" behavior unambiguous in tests
    classes = ["Tomato_Late_Blight"]
    for cls in classes:
        src_cls = src_root / cls
        dst_cls = tmp / cls
        dst_cls.mkdir(parents=True, exist_ok=True)
        # copy first 3 images
        imgs = sorted([p for p in src_cls.iterdir() if p.suffix.lower() in [".jpg", ".jpeg", ".png"]])[:3]
        assert imgs, f"No images found in {src_cls}"
        for p in imgs:
            shutil.copy2(p, dst_cls / p.name)

    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture()
def db_session():
    """
    Use an isolated SQLite DB per test, and override FastAPI dependency.
    """
    db_path = Path(tempfile.mkdtemp(prefix="agroai_db_")) / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def _get_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db_override

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        app.dependency_overrides.pop(get_db, None)
        shutil.rmtree(db_path.parent, ignore_errors=True)


@pytest.fixture()
def client(db_session) -> TestClient:
    return TestClient(app)


@pytest.fixture()
def configure_ml(monkeypatch, encoder_path, temp_train_dir):
    """
    Point ML service to the tiny dataset, then force re-init.
    """
    monkeypatch.setenv("ENCODER_PATH", encoder_path)
    monkeypatch.setenv("TRAIN_DATA_DIR", str(temp_train_dir))
    # For tiny test datasets, use a lower percentile so we don't over-reject in-distribution samples.
    monkeypatch.setenv("OPEN_SET_PERCENTILE", "0.1")
    # Keep TTA sample count aligned with inference (classifier uses 20 by default)
    monkeypatch.setenv("OPEN_SET_TTA_SAMPLES", "20")

    # backend.config.settings is instantiated at import time, so update it too
    from backend.config import settings
    settings.ENCODER_PATH = encoder_path
    settings.TRAIN_DATA_DIR = str(temp_train_dir)

    # Reset singleton state
    ml_service.classifier = None
    ml_service.prototypes = None
    ml_service.class_names = None
    ml_service.threshold = None

    ml_service.initialize()
    assert ml_service.classifier is not None
    assert ml_service.threshold is not None
    return ml_service


@pytest.fixture()
def auth_headers(client, db_session) -> dict:
    # Create a verified normal user directly in DB (auth flow uses email verification)
    from backend.models import User
    from backend.auth_utils import get_password_hash

    u = User(
        email="user@example.com",
        username="user",
        hashed_password=get_password_hash("password123"),
        is_admin=False,
        is_active=True,
        is_verified=True,
    )
    db_session.add(u)
    db_session.commit()

    r = client.post(
        "/api/v1/auth/login",
        data={"username": "user", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_headers(client, db_session) -> dict:
    # create admin user directly in DB
    from backend.models import User
    from backend.auth_utils import get_password_hash

    admin = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        is_admin=True,
        is_active=True,
        is_verified=True,
    )
    db_session.add(admin)
    db_session.commit()

    r = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

