import unittest
from src.matching.store_matcher import StoreMatcher

class TestStoreMatcher(unittest.TestCase):
    def test_store_match(self):
        stores = [
            {"store_code":"604445065","store_name":"通州区金沙润惠多超市","region":"East"},
            {"store_code":"10377868","store_name":"平阴百龙商厦","region":"North"},
        ]
        result = StoreMatcher(stores).match("通州区金沙润惠多超市")
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["match"]["store_code"], "604445065")

if __name__ == "__main__": unittest.main()
