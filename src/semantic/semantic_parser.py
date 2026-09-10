class SemanticParser:
    """Semantic parser interface for the public reference implementation.
    公开版本中的语义解析接口；生产 LLM 实现未包含在本仓库中。
    """
    def parse(self, batch_text: str) -> dict:
        raise NotImplementedError

class MockSemanticParser(SemanticParser):
    """Mock semantic parser used only for the public reference implementation.
    It follows the original business flow at a high level, but does not contain
    production prompts or model logic.
    """
    def parse(self, batch_text: str) -> dict:
        text = batch_text.replace("登记", "").strip()
        if not text or text in {"好的", "收到"}:
            return {"valid": False, "records": []}
        if "执行重点" in text or "不合格" in text or "达标" in text:
            category = "KPI/CEP规则配置"
        elif "堆" in text or "端架" in text or "陈列架" in text:
            category = "地堆数量"
        elif "组" in text and "货架" in text:
            category = "货架组数"
        elif "未识别" in text or "没识别" in text or "未在架" in text or "没显示" in text:
            category = "产品识别"
        else:
            return {"valid": False, "records": []}
        if "6900000000001" in text and "6900000000002" in text:
            return {"valid": True, "records": [
                {"问题描述": "样例商品未识别", "问题归类": "产品识别", "store_hint": "好多多超市三元店", "product_hint": "6900000000001", "brand_hint": "", "raw_evidence": text},
                {"问题描述": "样例商品未识别", "问题归类": "产品识别", "store_hint": "好多多超市三元店", "product_hint": "6900000000002", "brand_hint": "", "raw_evidence": text},
            ]}
        return {"valid": True, "records": [{
            "问题描述": "护舒宝执行重点为空，需核查规则配置" if "护舒宝" in text else text,
            "问题归类": category,
            "store_hint": "通州区金沙润惠多超市" if "通州区金沙润惠多超市" in text else "",
            "product_hint": "",
            "brand_hint": "护舒宝" if "护舒宝" in text else "",
            "raw_evidence": text,
        }]}
