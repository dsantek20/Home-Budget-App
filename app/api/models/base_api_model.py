from pydantic import BaseModel, ConfigDict

class BaseApiModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
