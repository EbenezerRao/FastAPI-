from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'postgresql://postgres:root@localhost:5432/demo_db'

engine = create_engine(DATABASE_URL, echo=True)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = LocalSession()
    try: 
        yield db
    finally:
        db.close()