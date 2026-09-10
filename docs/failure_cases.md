# Bad Cases / Failure Cases

以下案例均为 Synthetic / Fictional Cases，但业务逻辑来自原项目规则和历史测试样例。未使用真实客户数据。

All cases are synthetic and fictional, but the business logic is grounded in the original project rules and historical test patterns.

## Case 1：服务群补充被误当成问题 / Service-group note treated as a complaint

场景：

```text
通州区金沙润惠多超市护舒宝执行重点空了，麻烦看一下
合肥合鑫
登记
```

实际问题：`合肥合鑫` 是反馈服务群线索，不是新的客诉 record，也不应进入问题描述。

系统如何处理：生成一条 `KPI/CEP规则配置` record，服务群由规则映射补全。

为什么这样处理：服务群是批次级元信息，不能被拆成独立问题。

English: The service-group note is metadata, not a separate complaint record.

## Case 2：多门店同类问题需要拆多条 / Multiple stores in one batch

场景：

```text
平阴百龙织物基础实际执行2个堆，识别1.75
银座平阴店织物基础实际执行2个堆，识别2.25个
登记
```

实际问题：同一批次包含两个门店，各自有数量识别偏差。

系统如何处理：按门店拆成两条 `地堆数量` records，并分别匹配门店主数据。

为什么这样处理：不同门店不能合并为一条 record，否则后续定位和整改对象会错。

English: Different stores should produce separate records even if the issue type is the same.

## Case 3：多 SKU 未识别不能拼成一条 / Multiple unrecognized SKUs

场景：

```text
好多多超市三元店，这五个品没识别出来：6900000000001, 6900000000002
登记
```

实际问题：产品识别类 record 不能把多个 Barcode 拼接到一个字段里。

系统如何处理：按一 SKU 一 record 拆分，每条记录只包含一个 Barcode / PMS / 产品名称。

为什么这样处理：产品主数据和后续处理都以单个 SKU 为单位。

English: Product-recognition records must be finalized as one SKU per record.

## Case 4：文字范围优先于 OCR 扩展 / Text scope before OCR expansion

场景：

```text
姚王庄店海飞丝货架质量小于0.5，识别不合格
图片 OCR 同屏出现：海飞丝不合格、潘婷不合格
登记
```

实际问题：OCR 同屏信息包含多个品牌，但客户文字只反馈海飞丝。

系统如何处理：只生成海飞丝相关 record，潘婷 OCR 只保留为图片证据或上下文，不自动扩展为新工单。

为什么这样处理：客户文字优先级高于 OCR，同屏内容不等于投诉对象。

English: Customer text defines the complaint scope. OCR evidence should not automatically expand the record to unrelated brands.

## Case 5：门店短名可能误匹配 / Store short-name ambiguity

场景：

```text
京客隆甜水园店织物堆头显示不合格
登记
```

实际问题：用户常省略行政词或公司全称，短店名需要匹配主数据；但通用词如“超市/购物/店”不能主导匹配。

系统如何处理：从 `store_hint` 和上下文 token 召回候选，最终店铺名称和店铺编号来自主数据；无法唯一确认时，字段可留空并在回复中提示复核。

为什么这样处理：不能把 LLM 的短名或猜测直接写成标准门店。

English: Short store names are matching clues, not authoritative store identifiers.

## Case 6：反馈人员误抽取 / Feedback person extraction

场景：

```text
@内部同事 @外部反馈人 麻烦看下，宝敏瑞，登记
```

实际问题：内部人员和外部反馈人可能同时出现在 @ 提及里，不能把内部人员登记为反馈人员。

系统如何处理：排除内部人员和机器人账号，优先选择外部反馈人；无法确认时在回复中提示复核。

为什么这样处理：反馈人员字段要反映外部反馈来源，而不是登记或协助处理的内部人员。

English: The feedback person should represent the external feedback source, not internal staff mentioned in the message.
