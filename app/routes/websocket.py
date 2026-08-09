import json

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.services.connectionmanager import (
    ConnectionManager,
)


router = APIRouter()

manager = ConnectionManager()


@router.websocket(
    "/ws/{conversation_id}"
)
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: int,
    user_id: int | None = None,
):

    await manager.connect(
        conversation_id,
        websocket,
        user_id=user_id,
    )

    try:

        while True:

            try:
                data = await websocket.receive_json()
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "ERROR",
                    "message": "Invalid JSON payload"
                })
                continue

            if not isinstance(data, dict):
                continue

            incoming_user_id = data.get("user_id") or user_id

            await manager.broadcast(
                conversation_id,
                data,
                user_id=incoming_user_id,
            )

    except WebSocketDisconnect:

        manager.disconnect(
            conversation_id,
            websocket
        )