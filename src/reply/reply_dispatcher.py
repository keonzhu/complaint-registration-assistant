class ReplyDispatcher:
    """Reply dispatcher interface for the public reference implementation.
    公开版本中的结果回复接口；生产平台回复实现未包含在本仓库中。
    """
    def send(self, conversation_id: str, text: str) -> dict:
        raise NotImplementedError

class MockReplyDispatcher(ReplyDispatcher):
    def __init__(self):
        self.sent = []

    def send(self, conversation_id: str, text: str) -> dict:
        message_id = f"reply_{len(self.sent)+1:04d}"
        self.sent.append({"conversation_id": conversation_id, "message_id": message_id, "text": text})
        return {"ok": True, "message_id": message_id}
