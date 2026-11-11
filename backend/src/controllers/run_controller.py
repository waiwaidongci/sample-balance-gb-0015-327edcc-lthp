from src.models import WeightRun
from src.services.batch_service import get_batch
from src.services.run_service import queue,QUEUE,snapshot_inputs,detail,retry as retry_service
from src.utils.audit import record

def create(db,data,user):
    get_batch(db,data.batch_id)
    snapshot=snapshot_inputs(db,data.batch_id,data.tolerance,data.max_iterations,data.cap_ratio)
    row=WeightRun(**data.model_dump(),input_snapshot=snapshot,created_by=user.id);db.add(row);db.flush();record(db,user,'create_calibration',row.id);db.commit()
    try:queue.rpush(QUEUE,str(row.id))
    except Exception:row.status='failed';row.error='队列不可用，请稍后重试';db.commit()
    return detail(db,row.id)

def retry(db,run_id,user):
    result=retry_service(db,run_id);record(db,user,'retry_calibration',run_id);db.commit();return result
