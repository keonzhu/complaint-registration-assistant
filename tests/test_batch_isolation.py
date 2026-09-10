import unittest
from src.batch.batch_collector import BatchCollector, Message

class TestBatchIsolation(unittest.TestCase):
    def test_trigger_seals_batch_and_opens_new_one(self):
        c = BatchCollector()
        c.add_message(Message("c1", "m1", "first", 1))
        sealed = c.add_message(Message("c1", "m2", "登记", 2))
        self.assertTrue(sealed.sealed)
        self.assertEqual([m.message_id for m in sealed.messages], ["m1"])
        c.add_message(Message("c1", "m3", "next", 3))
        sealed2 = c.add_message(Message("c1", "m4", "登记", 4))
        self.assertEqual([m.message_id for m in sealed2.messages], ["m3"])

if __name__ == "__main__": unittest.main()
