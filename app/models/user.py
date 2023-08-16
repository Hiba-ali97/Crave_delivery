
from pydantic import BaseModel
class LoginCredentials(BaseModel):
    phone_number: str
    password: str