from dataclasses import dataclass

@dataclass
class IncomingMessage:
    platform: str
    conversation_id: str
    sender_id: str
    message_id: str
    timestamp: float
    type: str
    text: str = ""
    image_url: str | None = None
    quoted_message_id: str | None = None
