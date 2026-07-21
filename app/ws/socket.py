from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from typing import Dict
from services.web_socketmanager import ConnectionManager 
router = APIRouter()
connections: Dict[str, WebSocket] = {}

@router.websocket("/ws/{user_id}")
async def ws_endpoint(websocket: WebSocket, user_id: str):
    await ConnectionManager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            receiver = data["to"]

            await ConnectionManager.send_to_user(
                receiver,
                {
                    "from": user_id,
                    "message": data["message"]
                }
            )

    except WebSocketDisconnect:
        ConnectionManager.disconnect(user_id)
