from sqlalchemy import text
from app.db.session import engine


def test_oracle_connection():
    """Executes a simple query against Oracle DB to verify connectivity."""
    print("Connecting to Oracle Database...")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'Oracle DB Connected Successfully!' FROM DUAL"))
            message = result.scalar()
            print(f"SUCCESS: {message}")
    except Exception as e:
        print(f"ERROR: Failed to connect to Oracle Database.")
        print(f"Details: {e}")


if __name__ == "__main__":
    test_oracle_connection()