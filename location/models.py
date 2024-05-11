from sqlmodel import Field, SQLModel
from typing import Optional

class Signups(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str = Field(index=True)
    lastname:str 
    username:str
    email:str
    
class Logins(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email:str    
    
class Additems(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name:str 
    price:int
    description:str
    image:str      


   