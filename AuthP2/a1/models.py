from sqlalchemy import Column, Integer, String
from database import Base # Import the Base from the file you just made

class VaultUser(Base):
    # This is the actual name of the table inside PostgreSQL
    __tablename__ = "vault_users"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    
    # We set unique=True because no two users can have the same username
    username = Column(String, unique=True, index=True, nullable=False)
    
    # Storage limits and usage
    storage_limit_mb = Column(Integer, default=50)   # Default free tier is 50MB
    used_storage_mb = Column(Integer, default=0)     # Starts at 0MB used