"""Mock writer used only for the public reference implementation.
仅用于公开版本的参考实现。生产写表集成未包含在本仓库中。
"""

from .table_writer import TableWriter

class MockTableWriter(TableWriter):
    def __init__(self):
        self.records = []

    def create_record(self, record):
        record_id = f"rec_{len(self.records)+1:04d}"
        self.records.append({"record_id": record_id, **record})
        return {"ok": True, "record_id": record_id}
