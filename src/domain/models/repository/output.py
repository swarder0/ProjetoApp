import re
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator

from domain.models.common import (
    BaseModelEncoder, 
    AddressModel,
    ClientValidationErrors,
    PydanticObjectId,
    PyObjectId,
    )

class GeoPointModel(BaseModel):
    type_of: str = "Point"
    coordinates: Optional[list[Optional[float]]] = None


class PhoneModel(BaseModel):
    state_code: int
    country_code: int
    number: str

    @staticmethod
    def parse_phone(phone: str) -> "PhoneModel | None":
        results = re.match(r"^(\+?55)?(\d{2})(\d{8,9})$", phone)
        if results:
            country_code = int(results.group(1) or "55")
            state_code = int(results.group(2))
            number = results.group(3)
            return PhoneModel(state_code=state_code, country_code=country_code, number=number)
        else:
            return None
    
    def get_phone_str(self):
        return f"{self.country_code}{self.state_code}{self.number}"
    
class ArchiveModel(BaseModel):
    date: datetime
    reason: str

class EmailModel(BaseModel):
    address: str | None = None
    verified: bool = False

class ClientCadastro(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[str] = None
    cellphone: Optional[PhoneModel] = None
    address: Optional[AddressModel] = None
    password: Optional[str] = None
    email: Optional[EmailModel] = None

class ClientModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id", serialization_alias="_id")
    client: Optional[ClientCadastro] = None
    archived: Optional[ArchiveModel] = None
    geo_location: Optional[GeoPointModel] = None
    geo_city: Optional[str] = None
    geo_state: Optional[str] = None
    created_at: dict = Field(default_factory=lambda: {"date": datetime.now(), "user": "onboarding"})
    updated_at: list = Field(default_factory=lambda: [{"date": datetime.now(), "user": "onboarding"}])
    validations: list[ClientValidationErrors] = Field(default_factory=lambda: [])
    device_id: str
    device_type: str
    status: str
    terms_accepted: bool | None = False

    def has_validation_error_code(self, error_code: str):
        has_error = [error for error in self.validations if error_code == error.code]
        return has_error[0] if has_error else None
    
    def payload_for_account(self):
        client = self.client
        address = client.address
        cellphone = client.cellphone
        email = {
            "address": client.email.address if client.email else None,
            "verified": client.email.verified if client.email else False,
        }
        birth_date = client.birth_date
        payload = {
            "name": client.name,
            "preferred_name": client.name,
            "birth_date": birth_date,
            "email": email if email and email.get("address") else None,
            "phone":{
                "coutry_code": cellphone.country_code if cellphone else None,
                "state_code": cellphone.state_code if cellphone else None,
                "number": cellphone.number if cellphone else None,
            },
            "address": {
                "postal_code": address.zip_code if address else None,
                "street": address.street if address else None,
                "number": address.number if address else None,
                "complement": address.complement if address else None,
                "neighborhood": address.neighborhood if address else None,
                "city": address.city if address else None,
                "state": address.state if address else None,
                "state_acronym": address.state if address else None,
            },
            "password": {"password": client.password,},
            "device_type": self.device_type,
            "device_id": {"id": self.device_id},
        }
        return payload

class HashModel(BaseModelEncoder):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    key: str
    