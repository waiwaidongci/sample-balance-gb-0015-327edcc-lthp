from pydantic import BaseModel,Field
class UnitInput(BaseModel):
    code:str=Field(min_length=1,max_length=60,pattern=r'^[a-zA-Z0-9_-]+$')
    zone:str=Field(min_length=1,max_length=30)
    age_band:str=Field(min_length=1,max_length=30)
    mode:str=Field(min_length=1,max_length=30)
    trip_minutes:float=Field(ge=0,le=500,allow_inf_nan=False)
    base_weight:float=Field(default=1,gt=0,le=100,allow_inf_nan=False)
class CSVInput(BaseModel):
    csv_text:str=Field(min_length=10,max_length=1000000)
