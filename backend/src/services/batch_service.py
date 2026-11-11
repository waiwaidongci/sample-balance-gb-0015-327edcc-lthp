from sqlalchemy import select,func
from fastapi import HTTPException
from src.models import SampleBatch,SampleUnit,MarginTarget
from src.utils.serializers import serialize

def get_batch(db,batch_id):
    row=db.get(SampleBatch,batch_id)
    if not row:raise HTTPException(404,'样本批次不存在')
    return row

def list_batches(db):
    out=[]
    for row in db.scalars(select(SampleBatch).order_by(SampleBatch.id)):
        data=serialize(row)
        data['sample_count']=db.scalar(select(func.count()).select_from(SampleUnit).where(SampleUnit.batch_id==row.id))
        data['target_count']=db.scalar(select(func.count()).select_from(MarginTarget).where(MarginTarget.batch_id==row.id))
        out.append(data)
    return out
