from typing import Optional

from pydantic import BaseModel

from src.domain.models.repository.output import ClientModel

class StepModelOutput(BaseModel):
    next_step: str
    info: Optional[dict] = {}
    client: "ClientModel|None" = None