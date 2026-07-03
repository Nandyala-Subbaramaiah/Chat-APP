from fastapi import FastAPI
from app.database.session import engine
from app.database.base import Base

# import all models (VERY IMPORTANT)
from app.models import user, conversation, message

app = FastAPI()

Base.metadata.create_all(bind=engine)