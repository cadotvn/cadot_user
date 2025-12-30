"""
Startup script to initialize database and run the application.
"""
from app.db.init_db import init_db
from app.db.session import SessionLocal


def init() -> None:
    """Initialize the database."""
    db = SessionLocal()
    init_db(db)
    db.close()


def main() -> None:
    """Main function to initialize database."""
    print("Creating initial data...")
    init()
    print("Initial data created!")


if __name__ == "__main__":
    main()
