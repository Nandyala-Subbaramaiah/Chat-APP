# app/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. DATABASE URL (change this)
DATABASE_URL = "postgresql://username:password@localhost:5432/chatdb"

# 2. Engine (connects SQLAlchemy to DB)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# 3. SessionLocal (factory for DB sessions)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4. Dependency (used in FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()