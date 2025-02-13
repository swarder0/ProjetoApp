from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, field_validator
from validate_docbr import CPF

class CreateHashInput(BaseModel):
    name: str
    device_id: str
    device_type: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v
    
    @field_validator("name")
    @classmethod
    def name_length_must_not_exceed_150_characters(cls, v):
        if len(v) > 150:
            raise ValueError("Name length must not exceed 150 characters")
        return v

    @field_validator("name")
    @classmethod
    def name_must_contain_only_letters_and_spaces(cls, v):
        if not all(char.isalpha() or char.isspace() for char in v):
            raise ValueError("Name must contain only letters and spaces")
        return v

class CreateClientInput(BaseModel):
    device_id: str
    device_type: str
    terms_accepted: bool
    version: Optional[int] = None
    
    @field_validator("terms_accepted", mode="after")
    @classmethod
    def validate_terms_accepted(cls, v):
        if not v:
            raise ValueError("The terms and conditions must be accepted.")
        return v

class GeoLocationInput(BaseModel):
    long: Optional[float] = None
    lat: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None

class FullnameInput(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v
    
    @field_validator("name")
    @classmethod
    def name_length_must_not_exceed_150_characters(cls, v):
        if len(v) > 150:
            raise ValueError("Name length must not exceed 150 characters")
        return v

    @field_validator("name")
    @classmethod
    def name_must_contain_only_letters_and_spaces(cls, v):
        if not all(char.isalpha() or char.isspace() for char in v):
            raise ValueError("Name must contain only letters and spaces")
        return v

class BirthDateInput(BaseModel):
    birth_date: str

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid birth date format. Use YYYY-MM-DD")
        return v

class PhoneInput(BaseModel):
    coutry_code: str
    state_code: str
    number: str

    def get_phone_str(self):
        return f"+{self.coutry_code}{self.state_code}{self.number}"

class EmailInput(BaseModel):
    email: EmailStr

class PasswordInput(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not v.strip():
            raise ValueError("Password cannot be empty")
        return v

class AddressInput(BaseModel):
    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    zip_code: str

class GetClientInput(BaseModel):
    client_id: Optional[str] = None
    
    @field_validator("client_id", mode="after")
    @classmethod
    def check_valid_objectid(cls, v):
        if v and not ObjectId.is_valid(v):
            raise ValueError("The 'client_id' must be a valid ObjectId")
        return v

class ArchivedClientInput(BaseModel):
    client_id: str

    @field_validator("client_id", mode="after")
    @classmethod
    def check_valid_objectid(cls, v):
        if v and not ObjectId.is_valid(v):
            raise ValueError("The 'client_id' must be a valid ObjectId")
        return v