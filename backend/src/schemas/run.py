from pydantic import BaseModel,Field
class RunInput(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    batch_id:int=Field(gt=0)
    tolerance:float=Field(default=.001,ge=.000001,le=.05,allow_inf_nan=False)
    max_iterations:int=Field(default=200,ge=1,le=2000)
    cap_ratio:float=Field(default=8,ge=1,le=30,allow_inf_nan=False)
