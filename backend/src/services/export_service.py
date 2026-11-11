import csv,io
from fastapi import HTTPException
from sqlalchemy import select
from src.models import WeightReview
from .run_service import get_run

def export_csv(db,run_id):
    run=get_run(db,run_id)
    review=db.scalar(select(WeightReview).where(WeightReview.run_id==run_id,WeightReview.decision=='approved'))
    if not review:raise HTTPException(409,'请先由负责人批准权重口径，再导出交付')
    out=io.StringIO();out.write('\ufeff');writer=csv.writer(out)
    writer.writerow(['code','zone','age_band','mode','trip_minutes','base_weight','calibrated_weight','input_sha256'])
    for row in run.result['assignments']:
        vals=[row[k] for k in ['code','zone','age_band','mode','trip_minutes','base_weight']]
        vals=["'"+x if isinstance(x,str) and x.startswith(('=','+','-','@')) else x for x in vals]
        writer.writerow(vals+[round(row['weight'],8),run.result['checksum']])
    return out.getvalue()
