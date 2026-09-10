# 关键产品决策 / Key Product Decisions

## 1. 为什么需要 Batch / Why Batch is needed

中文：原项目中，一次登记往往由多条文字、图片、引用消息和服务群/反馈人补充共同构成。系统不能按 `1 message -> 1 record` 处理，而是先把同一会话中登记前的消息放入 batch，收到“登记”后封批。封批后，后续消息进入新批次。

English: One registration may consist of multiple texts, images, quoted messages, and service-group or feedback-person notes. The system groups messages into a batch before the trigger word `登记`; messages after the trigger belong to the next batch.

## 2. 为什么只有“登记”触发 / Why only one trigger word is used

中文：真实项目中，“提交/确认/录入”等词可能出现在普通业务描述中，不能作为封批触发词。当前口径只使用“登记”作为提交边界。

English: Words like “submit”, “confirm”, or “record” may appear in business text. The current workflow uses only `登记` as the sealing trigger.

## 3. 为什么 OCR 和语义解析分开 / Why OCR and semantic parsing are separated

中文：图片 OCR 主要提供证据，例如 SKU 列表、barcode、识别状态、门店截图上下文。语义解析负责结合文字、OCR 和引用消息判断成单、拆单、描述和问题归类。分开处理便于判断错误来自 OCR、语义解析还是后续字段补全。

English: OCR provides evidence such as SKU lists, barcodes, recognition status, and screenshot context. Semantic parsing combines text, OCR, and quoted messages to produce record drafts.

## 4. 为什么需要 record 拆分 / Why record splitting is needed

中文：同一批次可能包含多门店、单店多问题、多 SKU 未识别、编号列表等情况。真实规则按“一个门店 + 一个问题归类 + 一个主要投诉对象”拆分。客服动作、服务群补充和登记命令不生成 record。

English: A batch may contain multiple stores, multiple issue types, multiple unrecognized SKUs, or numbered items. Records are split by store, issue category, and main complaint object.

## 5. 为什么需要批次级共享字段 / Why batch-level shared fields are needed

中文：反馈服务群、反馈人员和登记人经常只在整批消息中的某一处出现。拆成多条 record 后，这些字段需要继承到相关子记录，不能因为某条子记录局部文本没有重复出现就留空。

English: Service group, feedback person, and registrar may appear once in a batch. After splitting, related records inherit these batch-level fields.

## 6. 为什么需要主数据匹配 / Why master-data matching is needed

中文：用户写的门店名和商品名经常是简称。LLM 只输出 `store_hint`、`product_hint`、`brand_hint` 等线索，标准店铺名称、店铺编号、Barcode、PMS 产品编码和产品名称必须由主数据匹配得到。

English: User-provided store and product names are often informal. The LLM provides hints; standard business fields must come from master-data matching.

## 7. 为什么校验提示不一定阻断写表 / Why validation notes do not always block writing

中文：当前产品口径是“流畅写表优先”。已成单但部分字段缺失或主数据无法唯一匹配时，可以写表并在回复中提示人工复核。公开版本用 validation notes 表达这一点，不实现完整生产复核流程。

English: The current product direction prioritizes registration flow. Some incomplete but valid records may be written with review notes in the reply. The public version models this as validation notes rather than a full review workflow.
