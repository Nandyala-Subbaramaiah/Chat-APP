from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.chat_db import get_db, init_db
from app.models import Conversation, ConversationMember, Message, User

from app.routes import users
from app.routes import messages
from app.routes import conversations
from app.routes import conversation_member
from app.routes import websocket
from app.routes import auth


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


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
app.include_router(
    websocket.router
)
app.include_router(
    auth.router
)
@app.get("/")
def home():
    return {
        "message": "FastAPI is running"
    }


@app.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {
        "message": "Database connected successfully 🚀"
    }