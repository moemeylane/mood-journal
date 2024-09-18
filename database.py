from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///reflectra.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Session = Session()
Base = declarative_base()

def init_db():
    """Initialize the database by creating tables."""
    Base.metadata.create_all(engine)
