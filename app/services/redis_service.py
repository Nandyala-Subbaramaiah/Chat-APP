import json
import os
from typing import Any, Dict, List

try:
    import redis
except ImportError:  # pragma: no cover - optional dependency in dev/test
    redis = None

REDIS_AVAILABLE = redis is not None
redis_client = None

if REDIS_AVAILABLE:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )

OFFLINE_MESSAGE_PREFIX = "offline_messages"
_IN_MEMORY_OFFLINE: Dict[str, List[Dict[str, Any]]] = {}


def _key(user_id: int) -> str:
    return f"{OFFLINE_MESSAGE_PREFIX}:{user_id}"


def _redis_healthy() -> bool:
    if not REDIS_AVAILABLE or redis_client is None:
        return False

    try:
        redis_client.ping()
        return True
    except Exception:
        return False


def push_offline_message(user_id: int, payload: Dict[str, Any]) -> bool:
    if user_id is None:
        return False

    key = _key(user_id)

    if _redis_healthy():
        try:
            redis_client.rpush(key, json.dumps(payload))
            return True
        except Exception:
            pass

    _IN_MEMORY_OFFLINE.setdefault(str(user_id), []).append(payload)
    return True


def pop_offline_messages(user_id: int) -> List[Dict[str, Any]]:
    if user_id is None:
        return []

    key = _key(user_id)

    if _redis_healthy():
        try:
            raw_items = redis_client.lrange(key, 0, -1)
            redis_client.delete(key)
            return [json.loads(item) for item in raw_items]
        except Exception:
            pass

    return _IN_MEMORY_OFFLINE.pop(str(user_id), [])
