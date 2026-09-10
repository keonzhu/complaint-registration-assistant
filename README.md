# AI Customer Complaint Registration Assistant

本仓库是基于真实客诉登记项目重新整理的脱敏案例与参考实现，不是生产源码。生产环境接口、企业内部代码、真实业务数据、完整 Prompt、平台配置、内部路径和敏感信息均未包含在公开版本中。公开代码只保留与真实业务流程一致的 Mock / Reference Implementation，用于说明 AI 产品设计、字段流转、主数据匹配、评测与 Bad Case 分析。

This repository is a sanitized case study and reference implementation derived from a real complaint-registration project. It is not production source code. Production integrations, proprietary code, real business data, full prompts, platform configurations, internal paths, and confidential information are intentionally excluded.

## 项目简介 / Overview

真实项目处理的是零售执行识别系统中的登记反馈。用户通常会把门店、服务群、反馈人、商品/品牌、图片 OCR 结果和问题描述一起转发给登记助手，再发送“登记”触发处理。

The original workflow is about registration feedback for retail execution recognition results. Users send store clues, service-group clues, feedback person information, product or brand clues, OCR evidence, and issue descriptions, then use a trigger word to submit the batch.

## 业务问题 / Problem

真实业务中的难点主要来自这些情况：

- 一批输入可能包含多条连续消息、引用消息和图片；
- 一批输入可能拆成 0/1/N 条 record；
- 图片 OCR 可能包含 SKU、barcode、货架/堆头识别状态、门店信息或截图上下文；
- 用户输入的门店名、商品名、服务群名经常是简称或非标准写法；
- “登记”是提交边界，“提交/确认/录入”等普通业务词不应触发封批；
- 客服寒暄、服务群补充、登记命令不应生成 record；
- 字段缺失或主数据无法唯一匹配时，当前产品口径优先保持登记流畅，写表后在回复中提示人工复核。

The main challenges are multi-message batching, OCR evidence, record splitting, informal store and product names, batch-level shared fields, and deterministic completion of standardized fields.

系统不是：

```text
Message -> LLM -> Business Table
```

更接近：

```text
WeCom-style DM / Forwarded Messages
  -> BatchStore
  -> Trigger Word: 登记
  -> OCR Evidence
  -> Semantic Record Parsing
  -> Field Completion
  -> Master Data Matching
  -> Base Writer Mock
  -> Reply with Registration Result / Review Notes
```

LLM 负责理解和拆分，标准字段由主数据、规则和字段校验补全。公开版本只保留这条业务流程的脱敏参考实现。

The LLM handles understanding and record splitting. Standardized fields are completed by rules, master data, and validation logic. The public version keeps this workflow as a sanitized reference implementation.

## 核心字段 / Core Record Fields

公开 demo 保留真实字段形态，但使用合成数据：

```text
问题描述
图片信息
Barcode
PMS产品编码
产品名称
品牌
问题归类
反馈服务群
反馈人员（微信名）
店铺名称
店铺编号
登记人
登记时间
```

问题归类使用真实项目中的类别口径：`KPI/CEP规则配置`、`货架组数`、`地堆数量`、`产品识别`、`完美货架/堆头问题`。公开 demo 仅覆盖其中一部分。

The public demo keeps the original field shape with synthetic data. It does not include real business records.

## AI 与程序边界 / AI vs Program Logic

LLM 实际负责：判断是否成单、拆分 records、生成问题描述、输出问题归类、抽取 `store_hint`、`product_hint`、`brand_hint` 等线索，并结合 OCR 和引用文本理解上下文。

Program logic handles batching, trigger detection, OCR handling, service-group and feedback-person extraction, registrar mapping, master-data matching, record finalization, writing, readback-style verification in production, and reply generation.

几个关键边界：

- 店铺名称和店铺编号必须来自门店主数据，不能直接使用模型补全的标准店名；
- 产品字段只在 `问题归类=产品识别` 时填写；
- Barcode / PMS / 产品名称来自产品主数据或明确 barcode 线索，不能由模型编造；
- 反馈服务群、反馈人员、登记人可以是批次级共享字段，被拆出的子记录继承；
- 校验失败当前不一定阻断写表，主要在回复中提示人工复核。

## 关键产品决策 / Key Product Decisions

详情见 `docs/product_decisions.md`。公开版本只保留原项目有依据的决策：Batch、OCR 与语义解析分工、record 拆分、批次级共享字段、主数据匹配、写表后复核提示。

See `docs/product_decisions.md` for product decisions grounded in the original project.

## 评测体系 / Evaluation Framework

详情见 `docs/evaluation.md`。公开版本仅展示合成评测样例和评测维度，不公开生产 metrics、内部测试数字或真实 bad case 数据。

See `docs/evaluation.md`. Production metrics, internal evaluation results, and real bad-case data are intentionally excluded.

## Bad Cases / Failure Cases

详情见 `docs/failure_cases.md`。所有案例都是 Synthetic / Fictional，但业务形态来自原项目规则：多门店拆单、服务群元信息不能成单、未在架 SKU 拆分、OCR 与文字范围冲突、门店短名误匹配、反馈人员误抽取。

See `docs/failure_cases.md`. All cases are synthetic, but the business logic follows the original project rules.

## 快速开始 / Quick Start

推荐 Python 3.11+。

Python 3.11+ is recommended.

```bash
pip install -r requirements.txt
pytest
python -m src.evaluation.run_eval examples/eval_cases.json examples/expected_outputs.json
python examples/demo.py
```

## 公开范围 / Repository Scope

公开内容 / Included:

- 脱敏业务流程 / Sanitized workflow
- Batch 与 trigger 参考实现 / Batch and trigger reference implementation
- OCR Mock / Mock OCR
- 语义解析 Mock / Mock semantic parser
- 字段补全与主数据匹配示例 / Field completion and master-data matching examples
- 合成样例和测试 / Synthetic examples and tests
- Prompt Design Specification / Prompt 设计说明

未公开内容 / Not included:

- 生产源码 / Production source code
- 完整生产 Prompt / Full production prompts
- 真实平台接口 / Production platform integrations
- 真实业务数据和主数据 / Real business data and master data
- 真实密钥、内部路径、企业配置 / Credentials, internal paths, and company-specific configurations
- 生产指标 / Production metrics

## 目录结构 / Repository Structure

```text
complaint-registration-assistant/
├── README.md
├── NOTICE.md
├── docs/
│   ├── architecture.md
│   ├── product_decisions.md
│   ├── evaluation.md
│   └── failure_cases.md
├── prompt_design/
│   ├── batch_record_parsing.md
│   ├── field_completion.md
│   └── invalid_input_filtering.md
├── src/
│   ├── batch/
│   ├── ocr/
│   ├── semantic/
│   ├── matching/
│   ├── validation/
│   ├── writer/
│   └── reply/
├── examples/
└── tests/
```

## 许可说明 / License Notice

本仓库暂不声明生产代码的开源许可证。公开版本是脱敏后重新实现的参考实现，最终许可证需由项目所有者确认。详见 `NOTICE.md`。

This repository does not claim an open-source license for production code. The public version is a sanitized reimplementation. See `NOTICE.md`.
