from src.batch.batch_collector import BatchCollector, Message

class MessageRouter:
    def __init__(self, collector: BatchCollector):
        self.collector = collector

    def route(self, incoming):
        msg = Message(
            conversation_id=incoming.conversation_id,
            message_id=incoming.message_id,
            text=incoming.text,
            ts=incoming.timestamp,
            type=incoming.type,
            image_url=incoming.image_url,
        )
        return self.collector.add_message(msg)
