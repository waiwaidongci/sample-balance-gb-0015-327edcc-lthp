from fastapi import APIRouter,Depends
from src.config.database import session
from src.middlewares.auth import current_user,require
from src.schemas.review import ReviewInput
from src.services.review_service import list_reviews
from src.controllers.review_controller import create
router=APIRouter(prefix='/reviews',tags=['review'])
@router.get('')
def listing(db=Depends(session),user=Depends(current_user)):return list_reviews(db)
@router.post('',status_code=201)
def creating(data:ReviewInput,db=Depends(session),user=Depends(require('admin'))):return create(db,data,user)
