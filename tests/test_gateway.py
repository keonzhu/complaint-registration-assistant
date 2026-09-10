import json, unittest
from src.gateway.webhook_adapter import parse_webhook_payload
from src.gateway.security import sign_payload, verify_signature

class TestGateway(unittest.TestCase):
    def test_parse_webhook_payload(self):
        msg = parse_webhook_payload(json.dumps({"conversation_id":"c","message_id":"m","timestamp":1,"text":"hello"}))
        self.assertEqual(msg.conversation_id, "c")
        self.assertEqual(msg.text, "hello")

    def test_signature(self):
        payload = b'{"ok":true}'
        sig = sign_payload(payload, "secret")
        self.assertTrue(verify_signature(payload, sig, "secret"))

if __name__ == "__main__": unittest.main()
