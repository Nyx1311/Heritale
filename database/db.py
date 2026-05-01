from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from config import Config

# Create the database engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# Create a scoped session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for models
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Initialize the database - create all tables"""
    import database.models
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def close_db():
    """Close database connection"""
    db_session.remove()
