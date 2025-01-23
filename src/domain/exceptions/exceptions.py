# Description: Exceptions for domain layer.
from typing import Any, Optional

from domain.models.enums import ErrorMessage, ErrorMessageMixin
class BaseNotFoundError(Exception):
    def __init__(self, param: dict, message: str):
        self.param = param
        self.message = message

class ClienteNotFoundError(BaseNotFoundError):
    def __init__(self, param: dict):
        super().__init__(param, "Client not found")