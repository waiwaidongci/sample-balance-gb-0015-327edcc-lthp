from sqlalchemy import select
from fastapi import HTTPException
from src.models import WeightRun
from src.config.queue import queue
from src.utils.serializers import serialize
from .batch_service import get_batch
from .unit_service import list_units
from .target_service import list_targets
from .raking_algorithm import calibrate
QUEUE='balance:calibration'

def get_run(db,run_id):
    row=db.get(WeightRun,run_id)
    if not row:raise HTTPException(404,'校准运行不存在')
    return row

def list_runs(db):return [serialize(x) for x in db.scalars(select(WeightRun).order_by(WeightRun.id.desc()))]

def detail(db,run_id):
    row=get_run(db,run_id);result=serialize(row);result['batch']=serialize(get_batch(db,row.batch_id));return result

def compute(db,run_id):
    run=get_run(db,run_id)
    if run.status=='completed':return
    run.status='running';db.commit()
    units=list_units(db,run.batch_id)
    targets=[{k:t[k] for k in ['dimension','category','population']} for t in list_targets(db,run.batch_id)]
    run.result=calibrate(units,targets,run.tolerance,run.max_iterations,run.cap_ratio)
    run.status='completed';run.error=None;db.commit()
