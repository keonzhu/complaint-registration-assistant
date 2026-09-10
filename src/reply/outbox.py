from dataclasses import dataclass
from typing import List

@dataclass
class OutboxItem:
    conversation_id: str
    text: str
    status: str = "pending"
    attempts: int = 0

class InMemoryOutbox:
    def __init__(self):
        self.items: List[OutboxItem] = []

    def enqueue(self, conversation_id: str, text: str):
        self.items.append(OutboxItem(conversation_id, text))

    def flush(self, dispatcher):
        for item in self.items:
            if item.status == "sent":
                continue
            item.attempts += 1
            result = dispatcher.send(item.conversation_id, item.text)
            item.status = "sent" if result.get("ok") else "failed"
