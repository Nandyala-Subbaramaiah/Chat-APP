from fastapi.testclient import TestClient
from app.database.chat_db import SessionLocal
from app.main import app
from app.models.conversation import Conversation
from app.models.users import User

db = SessionLocal()
try:
    user = User(username='alice-verify', email='alice-verify@example.com')
    db.add(user)
    db.commit()
    db.refresh(user)

    conversation = Conversation()
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    with TestClient(app) as client:
        with client.websocket_connect(f'/ws/{conversation.id}') as websocket:
            response = client.post(
                '/messages/',
                json={
                    'conversation_id': conversation.id,
                    'sender_id': user.id,
                    'message': 'hello live chat verify'
                }
            )
            print('HTTP_STATUS', response.status_code)
            payload = websocket.receive_json()
            print('WS_TYPE', payload.get('type'))
            print('WS_MESSAGE', payload.get('message', {}).get('message'))
            assert response.status_code == 200
            assert payload['type'] == 'NEW_MESSAGE'
            assert payload['message']['message'] == 'hello live chat verify'
            assert payload['message']['conversation_id'] == conversation.id
finally:
    db.close()
