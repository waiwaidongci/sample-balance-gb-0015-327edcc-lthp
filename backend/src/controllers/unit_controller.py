from src.services.unit_service import import_units
from src.utils.audit import record

def create(db,batch_id,data,user):
    count=import_units(db,batch_id,data.csv_text);record(db,user,'import_samples',str(batch_id)+':'+str(count));db.commit();return {'imported':count}
