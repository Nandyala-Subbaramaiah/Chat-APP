import json
from typing import Any, Dict, List

from fastapi import WebSocket

from app.services.redis_service import pop_offline_messages, push_offline_message


class ConnectionManager:

    def __init__(self):

        self.active_connections = {}


    async def connect(
        self,
        conversation_id: int,
        websocket: WebSocket,
        user_id: int | None = None,
    ):

        await websocket.accept()

        if conversation_id not in self.active_connections:

            self.active_connections[
                conversation_id
            ] = []

        self.active_connections[
            conversation_id
        ].append(websocket)

        if user_id is not None:
            await self.send_offline_messages(websocket, user_id)


    async def send_offline_messages(
        self,
        websocket: WebSocket,
        user_id: int,
    ):
        queued_messages = pop_offline_messages(user_id)
        for message in queued_messages:
            try:
                await websocket.send_json(message)
            except Exception:
                continue


    def disconnect(
        self,
        conversation_id: int,
        websocket: WebSocket
    ):

        if conversation_id in self.active_connections:

            if websocket in self.active_connections[
                conversation_id
            ]:

                self.active_connections[
                    conversation_id
                ].remove(websocket)


    async def broadcast(
        self,
        conversation_id: int,
        message: dict,
        user_id: int | None = None,
    ):

        connections = self.active_connections.get(
            conversation_id,
            []
        )

        if not connections and user_id is not None:
            push_offline_message(user_id, message)
            return

        for connection in connections:
            try:
                await connection.send_json(
                    message
                )
            except Exception:
                if user_id is not None:
                    push_offline_message(user_id, message)
                continue