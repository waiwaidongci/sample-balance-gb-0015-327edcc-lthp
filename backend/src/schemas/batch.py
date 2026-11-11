from pydantic import BaseModel,Field
class BatchInput(BaseModel):
    code:str=Field(min_length=2,max_length=60,pattern=r'^[a-z0-9-]+$')
    name:str=Field(min_length=2,max_length=100)
    description:str=Field(default='',max_length=500)
