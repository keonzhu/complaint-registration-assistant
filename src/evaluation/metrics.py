def accuracy(correct: int, total: int) -> float:
    return 0.0 if total == 0 else correct / total

def summarize(predictions, expected):
    total = len(expected)
    correct = 0
    for case_id, exp in expected.items():
        pred = predictions.get(case_id, {})
        if all(pred.get(k) == v for k, v in exp.items()):
            correct += 1
    return {"total": total, "correct": correct, "accuracy": accuracy(correct, total)}
