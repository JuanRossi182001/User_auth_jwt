from typing import Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class UserSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    
    class config:
        orm_mode = True
        
        
class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)
    
    
    
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]