"""
Script to create an admin user
"""
from backend.database import SessionLocal, init_db
from backend.models import User
from backend.auth_utils import get_password_hash

def create_admin():
    """Create an admin user"""
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@agroai.com").first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            email="admin@agroai.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),  # Change this password!
            full_name="System Administrator",
            is_admin=True,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        
        print("✅ Admin user created successfully!")
        print("Email: admin@agroai.com")
        print("Username: admin")
        print("Password: admin123")
        print("\n⚠️  IMPORTANT: Change the password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
