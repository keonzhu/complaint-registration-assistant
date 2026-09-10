from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Message:
    conversation_id: str
    message_id: str
    text: str
    ts: float
    type: str = "text"
    image_url: str | None = None

@dataclass
class Batch:
    conversation_id: str
    messages: List[Message] = field(default_factory=list)
    sealed: bool = False

class BatchCollector:
    """Collect messages belonging to the same complaint batch.
    收集属于同一客诉批次的连续消息。
    """
    def __init__(self, trigger_word: str = "登记"):
        self.trigger_word = trigger_word
        self._open: Dict[str, Batch] = {}

    def add_message(self, msg: Message):
        batch = self._open.setdefault(msg.conversation_id, Batch(msg.conversation_id))
        if msg.text.strip() == self.trigger_word:
            batch.sealed = True
            sealed = batch
            self._open[msg.conversation_id] = Batch(msg.conversation_id)
            return sealed
        batch.messages.append(msg)
        return None
