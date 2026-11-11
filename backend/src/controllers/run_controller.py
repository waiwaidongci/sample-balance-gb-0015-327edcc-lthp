from src.models import WeightRun
from src.services.batch_service import get_batch
from src.services.run_service import queue,QUEUE
from src.utils.audit import record
from src.utils.serializers import serialize

def create(db,data,user):
    get_batch(db,data.batch_id)
    row=WeightRun(**data.model_dump(),created_by=user.id);db.add(row);db.flush();record(db,user,'create_calibration',row.id);db.commit()
    try:queue.rpush(QUEUE,str(row.id))
    except Exception:row.status='failed';row.error='队列不可用，请重新创建';db.commit()
    return serialize(row)
