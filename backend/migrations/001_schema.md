# 初始数据结构
SQLAlchemy metadata创建schema；后续版本应新增真实迁移。唯一约束为sample_batches.code、sample_units(batch_id,code)、margin_targets(batch_id,dimension,category)、weight_reviews.run_id、users.email。不可用create_all做列变更。
