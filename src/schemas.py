from pydantic import BaseModel


class CreateUser(BaseModel):
    Username:str
    Password:str

class GetCredentials(BaseModel):
    Username:str
    Password:str
