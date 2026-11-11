from fastapi import APIRouter,Depends
from fastapi.responses import Response
from src.config.database import session
from src.middlewares.auth import current_user,require
from src.schemas.run import RunInput
from src.services.run_service import list_runs,detail
from src.services.export_service import export_csv
from src.controllers.run_controller import create,retry
router=APIRouter(prefix='/runs',tags=['calibration'])
@router.get('')
def listing(db=Depends(session),user=Depends(current_user)):return list_runs(db)
@router.post('',status_code=201)
def creating(data:RunInput,db=Depends(session),user=Depends(require('admin','analyst'))):return create(db,data,user)
@router.post('/{run_id}/retry')
def retrying(run_id:int,db=Depends(session),user=Depends(require('admin','analyst'))):return retry(db,run_id,user)
@router.get('/{run_id}')
def result(run_id:int,db=Depends(session),user=Depends(current_user)):return detail(db,run_id)
@router.get('/{run_id}/export')
def export(run_id:int,db=Depends(session),user=Depends(current_user)):return Response(export_csv(db,run_id),media_type='text/csv; charset=utf-8',headers={'Content-Disposition':f'attachment; filename="weights-{run_id}.csv"'})
