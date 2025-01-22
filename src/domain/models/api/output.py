from typing import Any, Optional


from domain.models.common import BaseModelEncoder
from domain.models.repository.output import ClientModel
from domain.models.usecases.output import StepModelOutput


class ApiResponseOutput(BaseModelEncoder):
    message: Optional[list[Any]] = None
    notice: Optional[list[Any]] = None
    data: StepModelOutput



class ClientResponseOutput(ApiResponseOutput):
    data: ClientModel
