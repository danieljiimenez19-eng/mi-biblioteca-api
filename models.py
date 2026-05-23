from pydantic import BaseModel

class Book(BaseModel):
    title : str
    author : str
    pages : int
    available : bool 

class User(BaseModel):
    email: str
    password : str
    
