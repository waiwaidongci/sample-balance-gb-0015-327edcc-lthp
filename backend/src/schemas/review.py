from typing import Literal
from pydantic import BaseModel,Field
class ReviewInput(BaseModel):
    run_id:int=Field(gt=0)
    decision:Literal['approved','rejected']
    note:str=Field(min_length=8,max_length=500)
