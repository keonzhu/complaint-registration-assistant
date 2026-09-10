from difflib import SequenceMatcher

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def _name(row):
    return row.get("store_name") or row.get("门店名称") or ""

def _code(row):
    return row.get("store_code") or row.get("store_id") or row.get("最终保留SEQ") or ""

class StoreMatcher:
    """Match store hints to synthetic master data.
    店铺标准字段来自主数据，不能由语义解析直接生成。
    """
    def __init__(self, stores):
        self.stores = stores

    def match(self, hint: str, region: str | None = None):
        candidates = []
        for row in self.stores:
            store_name = _name(row)
            score = similarity(hint, store_name) * 80
            if region and row.get("region") == region:
                score += 10
            if hint and hint.lower() in store_name.lower():
                score += 10
            candidates.append({**row, "store_name": store_name, "store_code": _code(row), "score": round(score, 2)})
        candidates.sort(key=lambda x: x["score"], reverse=True)
        if not candidates or candidates[0]["score"] < 60:
            return {"status": "needs_review", "candidates": candidates[:3]}
        return {"status": "matched", "match": candidates[0], "candidates": candidates[:3]}
