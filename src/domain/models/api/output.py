from typing import Any, Optional


from src.domain.models.common import BaseModelEncoder
from src.domain.models.repository.output import ClientModel
from src.domain.models.usecases.output import StepModelOutput


class ApiResponseOutput(BaseModelEncoder):
    message: Optional[list[Any]] = None
    notice: Optional[list[Any]] = None
    data: StepModelOutput

class HashOutput(BaseModelEncoder):
    key: str

class CreateHashApiResponseOutput(ApiResponseOutput):
    data: HashOutput

class ClientResponseOutput(ApiResponseOutput):
    data: ClientModel | dict

class CreateHashApiResponseOutput(ApiResponseOutput):
    data: HashOutput