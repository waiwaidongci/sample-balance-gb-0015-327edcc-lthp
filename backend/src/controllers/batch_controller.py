from sqlalchemy import select
from fastapi import HTTPException
from src.models import SampleBatch
from src.utils.audit import record
from src.utils.serializers import serialize

def create(db,data,user):
    if db.scalar(select(SampleBatch).where(SampleBatch.code==data.code)):raise HTTPException(409,'批次编码已存在')
    row=SampleBatch(**data.model_dump(),source_file='CSV文本导入');db.add(row);db.flush();record(db,user,'create_batch',row.code);db.commit();return serialize(row)
