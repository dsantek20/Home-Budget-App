from typing import Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: Optional[str] = None
    message: str
    debug_message: str | None = None