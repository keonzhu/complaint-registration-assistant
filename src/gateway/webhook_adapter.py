import json
from .schemas import IncomingMessage

def parse_webhook_payload(payload: str) -> IncomingMessage:
    data = json.loads(payload)
    return IncomingMessage(
        platform=data.get("platform", "generic"),
        conversation_id=data["conversation_id"],
        sender_id=data.get("sender_id", "unknown"),
        message_id=data["message_id"],
        timestamp=float(data["timestamp"]),
        type=data.get("type", "text"),
        text=data.get("text", ""),
        image_url=data.get("image_url"),
        quoted_message_id=data.get("quoted_message_id"),
    )
