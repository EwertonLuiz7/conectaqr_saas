from pydantic import BaseModel, Field, ConfigDict

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: str
    password: str

class ProfileIn(BaseModel):
    display_name: str = Field(default="", max_length=120)
    profession: str = Field(default="", max_length=160)
    bio: str = Field(default="", max_length=1200)
    whatsapp: str = Field(default="", max_length=30)
    email_public: str = Field(default="", max_length=255)
    website: str = Field(default="", max_length=500)
    instagram: str = Field(default="", max_length=500)
    is_published: bool = True

class QRCreateIn(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    destination_type: str = Field(default="profile")
    destination_value: str = Field(default="", max_length=1000)

class QRUpdateIn(BaseModel):
    title: str | None = Field(default=None, max_length=120)
    destination_type: str | None = None
    destination_value: str | None = Field(default=None, max_length=1000)
    is_active: bool | None = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    plan: str
    model_config = ConfigDict(from_attributes=True)

class ProfileOut(ProfileIn):
    slug: str
    model_config = ConfigDict(from_attributes=True)
