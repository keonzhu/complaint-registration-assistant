import csv
import json
import sys
from pathlib import Path

from src.batch.batch_collector import BatchCollector, Message
from src.matching.product_matcher import ProductMatcher
from src.matching.store_matcher import StoreMatcher
from src.reply.reply_dispatcher import MockReplyDispatcher
from src.semantic.semantic_parser import MockSemanticParser
from src.validation.field_validator import validate_record
from src.writer.mock_writer import MockTableWriter


def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def run_pipeline(data: dict, project_root: Path | None = None) -> dict:
    """Run the public reference pipeline on synthetic input.
    This uses only mock/reference components and does not call production services.
    """
    project_root = project_root or Path.cwd()
    collector = BatchCollector()
    sealed = None
    for raw in data['messages']:
        text = raw.get('text') or raw.get('ocr_text', '')
        sealed = collector.add_message(
            Message(
                data['conversation_id'],
                raw['id'],
                text,
                raw.get('timestamp', 0),
                raw.get('type', 'text'),
                raw.get('image_url'),
            )
        )
    if not sealed:
        return {'status': 'waiting_for_trigger', 'records': [], 'replies': []}

    batch_text = '\n'.join(m.text for m in sealed.messages)
    parsed = MockSemanticParser().parse(batch_text)
    stores = load_csv(project_root / 'examples/sample_master_stores.csv')
    products = load_csv(project_root / 'examples/sample_master_products.csv')
    writer = MockTableWriter()
    reply = MockReplyDispatcher()
    outputs = []

    for rec in parsed['records']:
        sm = StoreMatcher(stores).match(rec.get('store_hint', ''))
        pm = {'status': 'skipped'}
        if rec.get('问题归类') == '产品识别':
            pm = ProductMatcher(products).match(rec.get('product_hint', ''), brand=rec.get('brand_hint') or None)

        record = {
            '问题描述': rec.get('问题描述', ''),
            '图片信息': rec.get('raw_evidence', ''),
            'Barcode': '',
            'PMS产品编码': '',
            '产品名称': '',
            '品牌': rec.get('brand_hint', ''),
            '问题归类': rec.get('问题归类', ''),
            '反馈服务群': '合肥合鑫服务群' if '合肥合鑫' in batch_text else '',
            '反馈人员（微信名）': '张三' if '反馈人：张三' in batch_text else '',
            '店铺名称': '',
            '店铺编号': '',
            '登记人': data.get('registrar', ''),
            '登记时间': 'DEMO_TIME',
            'store_match_status': sm['status'],
            'product_match_status': pm['status'],
        }
        if 'match' in sm:
            record.update({'店铺名称': sm['match']['store_name'], '店铺编号': sm['match']['store_code']})
        if 'match' in pm:
            record.update({
                'Barcode': pm['match']['barcode'],
                'PMS产品编码': pm['match']['pms_code'],
                '产品名称': pm['match']['product_name'],
                '品牌': pm['match'].get('brand', record['品牌']),
            })
        record['validation_notes'] = validate_record(record)['notes']
        record['write_result'] = writer.create_record(record)
        outputs.append(record)

    reply.send(data['conversation_id'], f"登记完成：{len(outputs)} 条")
    return {'records': outputs, 'replies': reply.sent}


def main(messages_path='examples/sample_messages.json'):
    path = Path(messages_path)
    data = json.loads(path.read_text(encoding='utf-8'))
    project_root = path.resolve().parents[1] if path.is_absolute() else Path.cwd()
    print(json.dumps(run_pipeline(data, project_root), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'examples/sample_messages.json')
