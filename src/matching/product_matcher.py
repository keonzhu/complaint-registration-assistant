from difflib import SequenceMatcher

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def _barcode(row): return row.get("barcode") or row.get("Barcode") or ""
def _pms(row): return row.get("pms_code") or row.get("PMS产品编码") or row.get("产品编码") or ""
def _name(row): return row.get("product_name") or row.get("产品名称") or row.get("Name CN") or ""

class ProductMatcher:
    """Match product hints to synthetic product master data.
    Barcode/PMS/产品名称来自主数据或明确 barcode 线索。
    """
    def __init__(self, products):
        self.products = products

    def match(self, hint: str, barcode: str | None = None, brand: str | None = None):
        clue = barcode or (hint if hint and hint.isdigit() and len(hint) == 13 else None)
        if clue:
            for row in self.products:
                if _barcode(row) == clue:
                    item={**row,"barcode":_barcode(row),"pms_code":_pms(row),"product_name":_name(row),"score":100}
                    return {"status":"matched","match":item,"candidates":[item]}
        candidates=[]
        for row in self.products:
            pname=_name(row)
            score=similarity(hint, pname)*70
            if brand and row.get("brand","").lower()==brand.lower(): score+=15
            if hint and hint.lower() in pname.lower(): score+=15
            candidates.append({**row,"barcode":_barcode(row),"pms_code":_pms(row),"product_name":pname,"score":round(score,2)})
        candidates.sort(key=lambda x:x["score"], reverse=True)
        if not candidates or candidates[0]["score"] < 60:
            return {"status":"needs_review","candidates":candidates[:3]}
        return {"status":"matched","match":candidates[0],"candidates":candidates[:3]}
