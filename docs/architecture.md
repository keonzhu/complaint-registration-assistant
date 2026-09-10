# 系统架构 / Architecture

## 真实流程抽象 / Workflow grounded in the original project

中文：公开版本不连接真实平台和真实表格，只保留原项目中有依据的处理链路：消息进入、批次缓存、触发封批、OCR、语义拆单、字段补全、主数据匹配、写入和回复。

English: The public version does not connect to real platforms or tables. It keeps the grounded workflow from the original project: message intake, batch storage, trigger-based sealing, OCR, semantic record parsing, field completion, master-data matching, writing, and reply.

```text
Message Event
  -> BatchStore / BatchCollector
  -> Trigger Word: 登记
  -> OCR Evidence Attached by Message/Batch
  -> Semantic Parser Mock
  -> Record Drafts
  -> Batch-level Field Inheritance
  -> Store/Product Master Matching
  -> Field Validation Notes
  -> Mock Base Writer
  -> Reply Summary
```

## 模块说明 / Components

| 模块 / Component | 中文说明 | English |
|---|---|---|
| gateway | 将平台消息转为统一事件；公开版只保留 schema 和路由示例 | Normalizes message events; public version keeps schemas and routing examples |
| batch | 缓存同一会话内的多条消息，收到“登记”后封批 | Stores messages by conversation and seals a batch on `登记` |
| ocr | 保存图片 OCR 结果作为证据；公开版为 Mock | Keeps OCR text as evidence; mocked here |
| semantic | 参考实现中的 record parsing mock；生产 LLM Prompt 不公开 | Mock record parser; production prompts are excluded |
| matching | 用合成主数据匹配门店和产品字段 | Matches stores and products against synthetic master data |
| validation | 生成字段缺失或低置信提示；不模拟完整生产校验 | Produces missing-field or review notes; not full production validation |
| writer | Mock Base writer，只演示写表接口边界 | Mock writer showing the writer boundary |
| reply | 生成登记结果回复 | Generates a registration summary reply |

## 不包含的内容 / Exclusions

中文：不包含真实平台 adapter、真实 OCR 服务、真实 LLM 调用、真实 Base API、真实主数据、完整 Prompt、生产状态存储和真实日志。

English: Real platform adapters, OCR services, LLM calls, Base APIs, master data, full prompts, runtime state stores, and logs are excluded.
