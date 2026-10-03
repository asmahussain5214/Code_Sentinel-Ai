from app.db.session import engine, Base
import app.models  # Ensures all ORM models are loaded into Base metadata


def create_tables():
    """Drops and recreates all registered SQLAlchemy ORM models as tables in Oracle DB."""
    print("Initializing database tables in Oracle...")
    try:
        # Drop existing tables to ensure clean schema recreation
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("SUCCESS: Database tables created successfully!")
    except Exception as e:
        print(f"ERROR: Failed to create database tables.")
        print(f"Details: {e}")


if __name__ == "__main__":
    create_tables()