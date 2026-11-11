from src.services.review_service import review
from src.utils.audit import record
from src.utils.serializers import serialize

def create(db,data,user):
    row=review(db,data,user);record(db,user,'review_'+data.decision,row.run_id);db.commit();return serialize(row)
