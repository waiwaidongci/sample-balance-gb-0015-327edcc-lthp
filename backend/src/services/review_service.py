from sqlalchemy import select
from fastapi import HTTPException
from src.models import WeightReview
from src.utils.serializers import serialize
from .run_service import get_run

def list_reviews(db):return [serialize(x) for x in db.scalars(select(WeightReview).order_by(WeightReview.id.desc()))]

def review(db,data,user):
    run=get_run(db,data.run_id)
    if run.status!='completed':raise HTTPException(409,'仅可审核已完成运行')
    if data.decision=='approved' and not run.result.get('converged'):raise HTTPException(409,'未收敛权重不可批准，请调整边际或截断上限')
    if db.scalar(select(WeightReview).where(WeightReview.run_id==run.id)):raise HTTPException(409,'该运行已有审核记录')
    row=WeightReview(**data.model_dump(),reviewer_id=user.id);db.add(row);db.flush();return row
