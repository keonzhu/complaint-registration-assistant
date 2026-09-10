# 测评体系 / Evaluation Framework

生产环境业务指标与内部评测结果未包含在公开版本中。公开仓库只展示原项目对应的评测维度和合成 demo。

Production metrics and internal evaluation results are intentionally excluded. This repository only shows evaluation dimensions and synthetic demo cases.

## 原项目对应的评测维度 / Grounded evaluation dimensions

### 问题归类 / Category Classification

中文：检查问题是否被归到允许类别，如 `KPI/CEP规则配置`、`货架组数`、`地堆数量`、`产品识别`、`完美货架/堆头问题`。

English: Checks whether an issue is assigned to an allowed category.

### 无效信息过滤 / Routine or Invalid Input Filtering

中文：客服寒暄、服务群补充、登记命令、测试语句、纯元信息不应生成 record。

English: Greetings, service-group notes, trigger words, test messages, and metadata-only text should not generate records.

### record 拆分 / Record Splitting

中文：检查多门店、单店多问题、多 SKU、编号列表是否拆成正确数量的 records，同时避免把同一问题的补充说明过拆。

English: Checks splitting for multiple stores, multiple issues, multiple SKUs, and numbered lists while avoiding over-splitting follow-up details.

### 产品字段补全 / Product Field Completion

中文：仅 `问题归类=产品识别` 时填写 Barcode、PMS 产品编码、产品名称和品牌；多 SKU 需要一 SKU 一 record。

English: Product fields are filled only for product-recognition records. Multi-SKU cases should produce one record per SKU.

### 门店字段匹配 / Store Field Matching

中文：店铺名称和店铺编号必须来自主数据。短名、词序变化、SEQ、服务群、地址等信息只作为匹配线索。

English: Store name and code must come from master data. Short names, reordered words, SEQ clues, service groups, and addresses are matching signals.

### 批次与回复 / Batch and Reply

中文：检查“登记”封批、登记后消息进入新批次、OCR 归属正确、回复中包含成功信息和需复核字段。

English: Checks trigger-based sealing, post-trigger batch isolation, OCR attachment, and reply summaries with review notes.

## 合成 demo / Synthetic demo

```bash
python -m src.evaluation.run_eval examples/eval_cases.json examples/expected_outputs.json
```

该 demo 只验证评测 runner 和样例结构，不代表生产效果。

This demo only verifies the evaluation runner and sample structure. It does not represent production performance.
