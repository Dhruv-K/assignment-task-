from pydantic import BaseModel, EmailStr, constr


class SignupRequest(BaseModel):
    email: EmailStr
    full_name: constr(min_length=1)
    password: constr(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
