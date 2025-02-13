from typing import Optional, Union
from pydantic import BaseModel

from src.domain.models.api.input import (
    AddressInput,
    BirthDateInput,
    CreateClientInput,
    EmailInput,
    FullnameInput,
    PasswordInput,
    PhoneInput,
)
from src.domain.models.repository.output import ClientModel



class StepActivityInput(BaseModel):
    step_name: str
    step_data: Optional[Union[
        FullnameInput,
        AddressInput,
        EmailInput,
        PhoneInput,
        BirthDateInput,
        PasswordInput
    ]] = None
    client: ClientModel
    version: Optional[int] = None