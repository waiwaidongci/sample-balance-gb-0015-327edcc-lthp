from sqlalchemy import select,delete
from fastapi import HTTPException
from src.models import MarginTarget
from src.utils.serializers import serialize
from .batch_service import get_batch
from .unit_service import list_units
from .raking_algorithm import validate_targets

def list_targets(db,batch_id):
    get_batch(db,batch_id)
    return [serialize(x) for x in db.scalars(select(MarginTarget).where(MarginTarget.batch_id==batch_id).order_by(MarginTarget.dimension,MarginTarget.category))]

def replace_targets(db,batch_id,data):
    units=list_units(db,batch_id);targets=[x.model_dump() for x in data.targets]
    try:validate_targets(units,targets)
    except ValueError as e:raise HTTPException(422,str(e))
    db.execute(delete(MarginTarget).where(MarginTarget.batch_id==batch_id))
    for t in targets:db.add(MarginTarget(batch_id=batch_id,**t))
    return len(targets)
