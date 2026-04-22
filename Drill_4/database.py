from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABSASE_URL = 'sqlite:///./destinations.db'

engine = create_engine(DATABSASE_URL, connect_args={'check_same_thread': False})

LocalSession = sessionmaker(autoCommit=False, autoflush=False, bind=engine)

Base = declarative_base()
