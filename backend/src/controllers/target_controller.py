from src.services.target_service import replace_targets,list_targets
from src.utils.audit import record

def replace(db,batch_id,data,user):
    replace_targets(db,batch_id,data);record(db,user,'replace_targets',batch_id);db.commit();return list_targets(db,batch_id)
