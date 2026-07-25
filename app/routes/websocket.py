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

            data = await websocket.receive_json()

            await manager.broadcast(
                conversation_id,
                data
            )

    except WebSocketDisconnect:

        manager.disconnect(
            conversation_id,
            websocket
        )