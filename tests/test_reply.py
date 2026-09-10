import unittest
from src.reply.reply_dispatcher import MockReplyDispatcher
from src.reply.outbox import InMemoryOutbox

class TestReply(unittest.TestCase):
    def test_outbox_flush(self):
        outbox = InMemoryOutbox()
        outbox.enqueue("c1", "done")
        outbox.flush(MockReplyDispatcher())
        self.assertEqual(outbox.items[0].status, "sent")

if __name__ == "__main__": unittest.main()
