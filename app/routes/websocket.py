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
):

    await manager.connect(
        conversation_id,
        websocket
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

            await manager.broadcast(
                conversation_id,
                data
            )

    except WebSocketDisconnect:

        manager.disconnect(
            conversation_id,
            websocket
        )