from datetime import datetime

from litestar.dto import DTOConfig, DataclassDTO
from dataclasses import dataclass


@dataclass
class UserCreateDTO:
    name: str
    surname: str
    password: str


@dataclass
class UserUpdateDTO:
    name: str | None = None
    surname: str | None = None
    password: str | None = None


@dataclass
class UserResponseDTO:
    id: int
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime


class UserCreateDataclassDTO(DataclassDTO[UserCreateDTO]):
    config = DTOConfig(rename_strategy='camel')


class UserUpdateDataclassDTO(DataclassDTO[UserUpdateDTO]):
    config = DTOConfig(rename_strategy='camel')


class UserResponseDataclassDTO(DataclassDTO[UserResponseDTO]):
    config = DTOConfig(
        rename_strategy="camel"
    )
