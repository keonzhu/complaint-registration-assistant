import unittest
from src.evaluation.metrics import summarize

class TestEvaluationMetrics(unittest.TestCase):
    def test_accuracy(self):
        s = summarize({"a":{"x":1}, "b":{"x":2}}, {"a":{"x":1}, "b":{"x":3}})
        self.assertEqual(s["total"], 2)
        self.assertEqual(s["correct"], 1)
        self.assertEqual(s["accuracy"], 0.5)

if __name__ == "__main__": unittest.main()
