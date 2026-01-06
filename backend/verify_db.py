import sys
import os

# Add parent directory to path to allow importing backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import init_db, SessionLocal, engine
from backend.models import User
from backend.auth_utils import get_password_hash

def verify_database():
    print("1. Initializing Database...")
    try:
        init_db()
        print("   -> Success: Tables created (or already exist).")
    except Exception as e:
        print(f"   -> Failed: {e}")
        return

    print("\n2. Connecting to Database...")
    db = SessionLocal()
    try:
        print("   -> Success: Connection established.")
        
        # Check for existing test user
        test_email = "verify_test@example.com"
        existing_user = db.query(User).filter(User.email == test_email).first()
        
        if existing_user:
            print(f"\n3. Cleaning up previous test user...")
            db.delete(existing_user)
            db.commit()
            print("   -> Success: User deleted.")

        print("\n4. Creating Test User...")
        new_user = User(
            email=test_email,
            username="verify_test",
            hashed_password=get_password_hash("testpass123"),
            full_name="Test User",
            is_active=True
        )
        db.add(new_user)
        db.commit()
        print("   -> Success: User created.")

        print("\n5. Verifying User Persistence...")
        # New session to ensure we are reading from DB
        db.close()
        db = SessionLocal()
        
        user = db.query(User).filter(User.email == test_email).first()
        if user:
            print(f"   -> Success: User '{user.username}' found in database with ID {user.id}.")
        else:
            print("   -> Failed: User not found.")

        # Cleanup
        print("\n6. Final Cleanup...")
        db.delete(user)
        db.commit()
        print("   -> Success: Test user removed.")

    except Exception as e:
        print(f"\n   -> Error during verification: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_database()
