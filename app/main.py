from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.chat_db import get_db


from app.routes import users
from app.routes import messages
from app.routes import conversations
from app.routes import conversation_member



app = FastAPI()


# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(users.router)
app.include_router(messages.router)
app.include_router(conversations.router)
app.include_router(
    conversation_member.router
)

@app.get("/")
def home():
    return {
        "message": "FastAPI is running"
    }


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    return {
        "message": "Database connected successfully 🚀"
    }