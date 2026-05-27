from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABSE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABSE_URL, connect_args={"check_same_thread": False}
)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()