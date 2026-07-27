from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.services.connectionmanager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):

    await manager.connect(
        user_id,
        websocket,
    )

    try:

        while True:

            data = await websocket.receive_json()

            receiver = data["to"]

            message = {
                "from": user_id,
                "to": receiver,
                "message": data["message"],
            }

            await manager.send_to_user(
                receiver,
                message,
            )

    except WebSocketDisconnect:

        manager.disconnect(
            user_id,
        )