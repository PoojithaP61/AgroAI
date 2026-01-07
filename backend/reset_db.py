from backend.database import engine, Base, init_db
from backend.models import User, VerificationCode, Prediction, DiseaseHistory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """
    WARNING: This will drop ALL data in the database.
    Use this only when you need to reset the schema completely.
    """
    print("⚠️  WARNING: This will DELETE ALL DATA in the database.")
    confirm = input("Are you sure you want to proceed? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Operation cancelled.")
        return

    logger.info("Dropping all tables...")
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    logger.info("Tables dropped successfully.")

    logger.info("Recreating tables...")
    # Create all tables
    init_db()
    logger.info("Tables created successfully.")
    
    print("✅ Database reset complete.")

if __name__ == "__main__":
    reset_database()
