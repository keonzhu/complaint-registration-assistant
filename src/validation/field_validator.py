REQUIRED = ["问题描述", "问题归类"]

def validate_record(record):
    """Return review notes for the public reference implementation.
    当前产品口径偏向流畅登记；公开版用 notes 表达需复核项。
    """
    notes=[]
    for key in REQUIRED:
        if not record.get(key):
            notes.append(f"missing: {key}")
    if record.get("store_match_status") == "needs_review":
        notes.append("store master data not uniquely matched")
    if record.get("问题归类") == "产品识别" and record.get("product_match_status") == "needs_review":
        notes.append("product master data not uniquely matched")
    return {"status":"pass" if not notes else "review", "notes":notes}
