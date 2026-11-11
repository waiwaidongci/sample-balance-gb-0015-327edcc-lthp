from datetime import datetime
from sqlalchemy import select,update
from fastapi import HTTPException
from src.models import WeightRun,WeightReview
from src.config.queue import queue
from src.utils.serializers import serialize
from .batch_service import get_batch
from .unit_service import list_units
from .target_service import list_targets
from .raking_algorithm import calibrate,input_checksum,UNIT_KEYS,TARGET_KEYS
QUEUE='balance:calibration'
NO_SNAPSHOT_ERROR='该任务缺少创建时的原始输入快照（历史任务），无法重算；请新建校准任务'

def get_run(db,run_id):
    row=db.get(WeightRun,run_id)
    if not row:raise HTTPException(404,'校准运行不存在')
    return row

def _snapshot_of(row):
    snapshot=row.input_snapshot or {}
    return snapshot if snapshot.get('units') and snapshot.get('targets') else None

def _public(row,with_input=False):
    data=serialize(row);snapshot=_snapshot_of(row);data.pop('input_snapshot',None)
    data['has_snapshot']=snapshot is not None
    if with_input and snapshot:
        data['input']={k:snapshot.get(k) for k in ['sample_count','target_count','checksum','captured_at']}
    return data

def list_runs(db):return [_public(x) for x in db.scalars(select(WeightRun).order_by(WeightRun.id.desc()))]

def detail(db,run_id):
    row=get_run(db,run_id);result=_public(row,with_input=True);result['batch']=serialize(get_batch(db,row.batch_id));return result

def snapshot_inputs(db,batch_id,tolerance,max_iterations,cap_ratio):
    """创建任务时冻结样本、目标与参数；之后补录或调标不影响本任务。"""
    units=[{k:u[k] for k in UNIT_KEYS} for u in list_units(db,batch_id)]
    targets=[{k:t[k] for k in TARGET_KEYS} for t in list_targets(db,batch_id)]
    return {'version':1,'batch_id':batch_id,'captured_at':datetime.utcnow().isoformat(),
        'params':{'tolerance':tolerance,'max_iterations':max_iterations,'cap_ratio':cap_ratio},
        'units':units,'targets':targets,'sample_count':len(units),'target_count':len(targets),
        'checksum':input_checksum(units,targets,tolerance,max_iterations,cap_ratio)}

def _approved_exists(db,run_id):
    return db.scalar(select(WeightReview.id).where(WeightReview.run_id==run_id,WeightReview.decision=='approved')) is not None

def compute(db,run_id):
    run=get_run(db,run_id)
    if run.status=='completed':return
    snapshot=_snapshot_of(run)
    if not snapshot:
        run.status='failed';run.error=NO_SNAPSHOT_ERROR;db.commit();return
    if _approved_exists(db,run_id):return
    params=snapshot.get('params') or {}
    tolerance=params.get('tolerance',run.tolerance);max_iterations=params.get('max_iterations',run.max_iterations);cap_ratio=params.get('cap_ratio',run.cap_ratio)
    claimed=db.execute(update(WeightRun).where(WeightRun.id==run_id,WeightRun.status.in_(['queued','failed'])).values(status='running',error=None))
    db.commit()
    if claimed.rowcount!=1:return
    result=calibrate(snapshot['units'],snapshot['targets'],tolerance,max_iterations,cap_ratio)
    written=db.execute(update(WeightRun).where(WeightRun.id==run_id,WeightRun.status=='running',WeightRun.id.notin_(select(WeightReview.run_id).where(WeightReview.decision=='approved'))).values(result=result,status='completed',error=None))
    db.commit()
    if written.rowcount!=1:raise RuntimeError('结果写回冲突：任务状态已被改变，放弃重复结果')

def mark_failed(db,run_id,message):
    """仅把仍处 running 的任务标记失败；不覆盖已完成或他人持有的状态。"""
    db.execute(update(WeightRun).where(WeightRun.id==run_id,WeightRun.status=='running').values(status='failed',error=str(message)[:500]))
    db.commit()

def retry(db,run_id):
    run=get_run(db,run_id)
    if not _snapshot_of(run):raise HTTPException(409,NO_SNAPSHOT_ERROR)
    if _approved_exists(db,run_id):raise HTTPException(409,'该运行已批准交付，权重与导出内容不可变更，不能重算')
    moved=db.execute(update(WeightRun).where(WeightRun.id==run_id,WeightRun.status=='failed').values(status='queued',error=None))
    db.commit()
    if moved.rowcount!=1:raise HTTPException(409,'仅失败状态的任务可重试，请刷新确认当前状态')
    try:queue.rpush(QUEUE,str(run_id))
    except Exception:
        db.execute(update(WeightRun).where(WeightRun.id==run_id,WeightRun.status=='queued').values(status='failed',error='队列不可用，请稍后重试'));db.commit()
        raise HTTPException(503,'队列不可用，请稍后重试')
    return detail(db,run_id)
