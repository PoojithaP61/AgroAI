import sys
import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine, SessionLocal
from backend.models import User, Prediction, DiseaseHistory

def view_data():
    db = SessionLocal()
    try:
        print("="*60)
        print(f"DATABASE LOCATION: {os.path.abspath('backend/agroai.db')}")
        print("="*60)

        # 1. Users
        print("\n--- USERS TABLE ---")
        users = db.query(User).all()
        if not users:
            print("No users found.")
        for user in users:
            print(f"ID: {user.id} | Username: {user.username} | Email: {user.email} | Role: {'Admin' if user.is_admin else 'User'}")

        # 2. Predictions
        print("\n--- PREDICTIONS TABLE ---")
        predictions = db.query(Prediction).all()
        if not predictions:
            print("No predictions found.")
        for p in predictions:
            print(f"ID: {p.id} | Disease: {p.disease_name} | Crop: {p.crop_type} | Conf: {p.confidence_score:.2f}")

        # 3. Disease History (Stats)
        print("\n--- DISEASE HISTORY (STATS) ---")
        history = db.query(DiseaseHistory).all()
        if not history:
            print("No history stats found.")
        for h in history:
            print(f"Disease: {h.disease_name} | Total Detections: {h.total_detections} | Avg Conf: {h.avg_confidence:.2f}")

    except Exception as e:
        print(f"Error viewing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    view_data()
