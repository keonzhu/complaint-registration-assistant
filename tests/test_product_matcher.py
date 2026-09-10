import unittest
from src.matching.product_matcher import ProductMatcher

class TestProductMatcher(unittest.TestCase):
    def test_barcode_exact_match(self):
        products = [{"barcode":"6900000000001","pms_code":"PMS001","product_name":"样例洗发水930g","brand":"飘柔"}]
        result = ProductMatcher(products).match("6900000000001")
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["match"]["pms_code"], "PMS001")
        self.assertEqual(result["match"]["score"], 100)

if __name__ == "__main__": unittest.main()
