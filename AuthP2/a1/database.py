from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. The PostgreSQL Connection String
# Format: postgresql://<username>:<password>@<host>/<database_name>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost/vaultdrive"

# 2. The Engine (The physical cable to the database)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. The Session Factory (Creates temporary windows to talk to the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base Class (All your models will inherit from this)
Base = declarative_base()

# 5. The Memory Manager (The Dependency you inject into your routes)
def get_db():
    db = SessionLocal()
    try:
        yield db  # Hands the connection to the route
    finally:
        db.close()  # Automatically closes the connection when the route is done