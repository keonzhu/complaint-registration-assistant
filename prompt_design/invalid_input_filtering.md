# 无效输入过滤 / Invalid Input Filtering

Full production prompts are intentionally omitted.

## 任务 / Task

中文：识别不应登记的输入，例如客服寒暄、纯服务群补充、登记命令、测试语句、没有真实问题语义的文本。

English: Identify input that should not be registered, such as greetings, service-group-only notes, trigger words, test messages, or text without a real issue.

## 示例 / Synthetic Examples

```text
好的，收到 -> no record
合肥合鑫，登记 -> no record unless there is a real issue in the same batch
这个分销有的，但是没有识别出来 -> product-recognition record
```
