from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    is_superuser: bool

class UserCreateUpdate(UserBase):
    password: str


class UserRepresentation(UserBase):
    id: int
    is_active: bool