import json
import sys
from pathlib import Path
from src.app.demo_pipeline import run_pipeline
from .metrics import summarize

def case_to_messages(case: dict) -> dict:
    lines = [line.strip() for line in case.get('input', '').splitlines() if line.strip()]
    if not lines:
        lines = [case.get('input', '')]
    messages = []
    for idx, line in enumerate(lines, 1):
        messages.append({'id': f"{case['case_id']}_m{idx}", 'type': 'text', 'timestamp': idx, 'text': line})
    if not any(m['text'].strip() == '登记' for m in messages):
        messages.append({'id': f"{case['case_id']}_trigger", 'type': 'text', 'timestamp': len(messages) + 1, 'text': '登记'})
    return {'conversation_id': case['case_id'], 'registrar': 'Synthetic User', 'messages': messages}

def prediction_from_pipeline(result: dict) -> dict:
    records = result.get('records', [])
    first = records[0] if records else {}
    return {
        '问题归类': first.get('问题归类', ''),
        '店铺编号': first.get('店铺编号', ''),
        'record_count': len(records),
    }

def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python -m src.evaluation.run_eval examples/eval_cases.json examples/expected_outputs.json')
    project_root = Path.cwd()
    cases = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    expected = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    predictions = {}
    for case in cases:
        result = run_pipeline(case_to_messages(case), project_root)
        predictions[case['case_id']] = prediction_from_pipeline(result)
    print(json.dumps(summarize(predictions, expected), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
