from fastapi import WebSocket, APIRouter
from typing import Dict

router = APIRouter()
connections: Dict[str, WebSocket] = {}

@router.websocket("/ws/{user_id}")
async def ws_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            receiver = data["receiver"]
            if receiver in connections:
                await connections[receiver].send_json(data)
    except:
        del connections[user_id]
