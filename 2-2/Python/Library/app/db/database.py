from typing import Generator
from sqlmodel import SQLModel, create_engine, Session, inspect
from app.config import get_settings
from app.utils.logger import setup_logger
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
import os

settings = get_settings()
logger = setup_logger(settings.LOG_LEVEL)

logger.info("DATABASE_URL: %s", settings.DATABASE_URL)

def get_engine() -> Engine:
    if os.getenv("ENVIRONMENT") == "test":
        return create_engine(
            settings.DATABASE_TEST_URL,
            echo=True,
            poolclass=StaticPool,
        )
    return create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    try:
        # Import all models to ensure they're registered with SQLModel
        from app.models.book import Book
        from app.models.author import Author
        from app.models.category import Category
        from app.models.user import User
        from app.models.borrowed_book import BorrowedBook
        from app.models.associations import BookAuthor, BookCategory

        # Test database connection
        with get_engine().connect() as conn:
            logger.info("Database connection successful")

        # Log registered models
        logger.info("Registered models: %s", SQLModel.metadata.tables.keys())

        # Create tables
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(get_engine())
        logger.info("Database tables created successfully")

        # Verify tables
        inspector = inspect(get_engine())
        existing_tables = inspector.get_table_names()
        logger.info("Existing tables: %s", existing_tables)

        # Check for expected tables
        expected_tables = [
            "book", "author", "category", "user", 
            "borrowed_book", "bookauthor", "bookcategory"
        ]
        for table in expected_tables:
            if table not in existing_tables:
                logger.error(f"Table '{table}' was not created")
            else:
                logger.info(f"Table '{table}' exists")

    except Exception as e:
        logger.error("Error creating tables: %s", str(e))
        raise

def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        try:
            yield session
        except Exception as e:
            logger.error("Session error: %s", str(e))
            session.rollback()
            raise
        finally:
            session.close()

def init_db():
    create_db_and_tables()