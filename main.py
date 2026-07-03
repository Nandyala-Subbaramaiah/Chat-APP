from fastapi import FastAPI

from database import Base, engine

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# Root route
@app.get("/")
def read_root():
    return {"message": "Chat app is running!"}
