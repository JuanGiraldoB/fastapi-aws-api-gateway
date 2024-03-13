from pydantic import BaseModel, ConfigDict


# Dog classes
class DogBase(BaseModel):
    name: str
    breed: str


class DogCreate(DogBase):
    pass


class Dog(DogBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True

# User classes


class UserBase(BaseModel):
    email: str
    name: str
    contact_info: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    dogs: list[Dog]

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True
