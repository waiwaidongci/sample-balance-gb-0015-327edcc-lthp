# 002 校准任务输入快照

`weight_runs` 新增 `input_snapshot JSON NULL`：创建任务时冻结样本、目标与参数（含输入SHA256），计算与失败重试只读取该快照；之后批次补录样本或调整目标不影响已排队/已完成任务。

```sql
ALTER TABLE weight_runs ADD COLUMN input_snapshot JSON NULL;
```

应用启动时会对 MySQL 自动补齐该列（幂等）；新建库由 metadata 直接建出。

旧行该列为 NULL：历史任务照常查看，但因缺少原始输入不得重算——重试接口返回 409，worker 也会将其标记为失败并注明原因。已批准（approved）的运行禁止重算，结果与导出内容不可变更。
