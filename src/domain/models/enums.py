from dataclasses import dataclass
from enum import Enum



class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"
class StepNames(str, Enum):
    FULLNAME = "fullname"
    EMAIL = "email"
    PASSWORD = "password"
    PHONE = "phone"
    ADDRESS = "address"
    BIRTH_DATE = "birth_date"
class ClientStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
@dataclass
class ErrorMessageMixin:
    code: str
    message: str

class ErrorMessage(ErrorMessageMixin):
    pass
