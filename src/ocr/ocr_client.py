class OCRClient:
    """OCR client interface for the public reference implementation.
    公开版本中的 OCR 接口；生产 OCR 集成未包含在本仓库中。
    """
    def recognize(self, image_url: str) -> dict:
        raise NotImplementedError

class MockOCRClient(OCRClient):
    def recognize(self, image_url: str) -> dict:
        return {"ocr_text": "Sample Product 500ml barcode 6900000000001", "latency_ms": 850, "provider": "mock"}
