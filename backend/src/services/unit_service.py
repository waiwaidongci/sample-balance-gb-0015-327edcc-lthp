import io,csv
from sqlalchemy import select
from fastapi import HTTPException
from pydantic import ValidationError
from src.models import SampleUnit
from src.schemas.unit import UnitInput
from src.utils.serializers import serialize
from .batch_service import get_batch

def list_units(db,batch_id):
    get_batch(db,batch_id)
    return [serialize(x) for x in db.scalars(select(SampleUnit).where(SampleUnit.batch_id==batch_id).order_by(SampleUnit.code))]

def import_units(db,batch_id,csv_text):
    get_batch(db,batch_id)
    try:
        parsed=[UnitInput.model_validate(x) for x in csv.DictReader(io.StringIO(csv_text.lstrip('\ufeff')))]
    except (ValidationError,ValueError):raise HTTPException(422,'CSV字段或数值无效：需要code/zone/age_band/mode/trip_minutes/base_weight')
    if not parsed or len(parsed)>5000:raise HTTPException(422,'CSV需要1–5000行')
    codes=[x.code for x in parsed]
    if len(set(codes))!=len(codes):raise HTTPException(422,'CSV样本编号重复')
    existing=set(db.scalars(select(SampleUnit.code).where(SampleUnit.batch_id==batch_id)))
    if existing&set(codes):raise HTTPException(409,'存在已导入的样本编号，整批未写入')
    if len(existing)+len(parsed)>5000:raise HTTPException(422,'每批最多5000条')
    for row in parsed:db.add(SampleUnit(batch_id=batch_id,**row.model_dump()))
    return len(parsed)
