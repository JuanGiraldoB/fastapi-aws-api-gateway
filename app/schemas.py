from pydantic import BaseModel


# Dog classes
class DogBase(BaseModel):
    name: str
    breed: str


class DogCreate(DogBase):
    pass


class Dog(DogBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True
