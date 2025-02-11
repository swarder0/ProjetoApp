# Description: Exceptions for domain layer.
from typing import Any, Optional

from src.domain.models.enums import ErrorMessage, ErrorMessageMixin
class BaseNotFoundException(Exception):
    def __init__(self, param: dict, message: str):
        self.param = param
        self.message = message

class ClientNotFoundException(BaseNotFoundException):
    def __init__(self, param: dict):
        super().__init__(param, "Client not found")