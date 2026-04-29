from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The Blueprint: postgresql://<username>:<password>@<host>:<port>/<database_name>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/hackathon_db"
# echo=True means SQLAlchemy will print the raw SQL to your terminal!
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This is the dependency that hands a database connection to your routes
def get_db():
    db = LocalSession ()
    try:
        yield db
    finally:
        db.close()