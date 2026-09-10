# 字段线索与补全 / Field Hints & Completion

Full production prompts are intentionally omitted.

出于保密和知识产权保护要求，本仓库不包含生产环境完整 Prompt，仅展示脱敏后的任务定义。

## 任务 / Task

中文：LLM 输出门店、商品、品牌等线索；程序根据规则、上下文和主数据补全标准字段。

English: The LLM outputs store, product, and brand hints. Program logic completes standardized fields using rules, context, and master data.

## 关键字段 / Key fields

- `store_hint` -> `店铺名称` / `店铺编号`
- `product_hint` -> `Barcode` / `PMS产品编码` / `产品名称`
- `brand_hint` -> `品牌`
- batch-level service group -> `反馈服务群`
- external mentioned user -> `反馈人员（微信名）`
- submitting user -> `登记人`

## 约束 / Constraints

中文：标准门店和产品字段必须来自主数据。非 `产品识别` 类记录不填写 Barcode、PMS 产品编码和产品名称。

English: Standard store and product fields must come from master data. Barcode, PMS code, and product name are filled only for product-recognition records.
