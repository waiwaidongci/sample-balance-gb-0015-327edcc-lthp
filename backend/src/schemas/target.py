from pydantic import BaseModel,Field
from src.constants.enums import Dimension
class TargetInput(BaseModel):
    dimension:Dimension
    category:str=Field(min_length=1,max_length=30)
    population:float=Field(ge=0,le=100000000,allow_inf_nan=False)
class TargetSetInput(BaseModel):
    targets:list[TargetInput]=Field(min_length=2,max_length=60)
