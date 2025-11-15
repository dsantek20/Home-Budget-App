from pydantic import BaseModel

class BaseApiModel(BaseModel):

    class Config:
        from_attributes = True

