# 批次理解与 record 拆分 / Batch Understanding & Record Splitting

Full production prompts are intentionally omitted.

出于保密和知识产权保护要求，本仓库不包含生产环境完整 Prompt，仅展示脱敏后的任务定义。

## 任务 / Task

中文：基于同一 batch 的文字、引用消息、OCR 文本和消息顺序，判断是否成单，并输出 0/1/N 条 records 草稿。

English: Given batch text, quoted messages, OCR text, and message order, decide whether the batch contains registerable issues and output 0/1/N draft records.

## 输出 / Output

```json
{
  "records": [
    {
      "问题描述": "string",
      "问题归类": "KPI/CEP规则配置|货架组数|地堆数量|产品识别|完美货架/堆头问题",
      "store_hint": "string|null",
      "product_hint": "string|null",
      "brand_hint": "string|null",
      "raw_evidence": "string"
    }
  ]
}
```

## 约束 / Constraints

中文：`登记` 不进入问题描述；服务群补充、客服寒暄、登记命令不生成 record；多门店、多问题、多 SKU 需要按真实对象拆分；同一问题的补充说明不要过拆。

English: The trigger word should not appear in the description. Metadata and greetings should not create records. Split by real store, issue, or SKU objects, but avoid over-splitting follow-up explanations.
