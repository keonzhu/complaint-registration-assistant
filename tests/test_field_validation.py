import unittest
from src.validation.field_validator import validate_record

class TestFieldValidation(unittest.TestCase):
    def test_missing_description_adds_review_note(self):
        result = validate_record({"问题归类":"产品识别"})
        self.assertEqual(result["status"], "review")
        self.assertIn("missing: 问题描述", result["notes"])

    def test_complete_record_passes(self):
        result = validate_record({"问题归类":"KPI/CEP规则配置", "问题描述":"护舒宝执行重点为空"})
        self.assertEqual(result["status"], "pass")

if __name__ == "__main__": unittest.main()
