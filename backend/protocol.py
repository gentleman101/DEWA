import uuid
from datetime import datetime

def create_message(intent: str, agent_id: str, payload: dict):
    return {
        "protocol": "ACP/1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "intent": intent,
        "agent_id": agent_id,
        "payload": payload
    }

def create_response(status: str, data):
    return {
        "protocol": "ACP/1.0",
        "status": status,
        "data": data
    }