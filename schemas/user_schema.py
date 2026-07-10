from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=100)
