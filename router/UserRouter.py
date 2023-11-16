from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from starlette import status
from config.config import sessionLocal
from model.User import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from schema.UserSchema import RequestUser
from model.Token import Token
from service.UserService import create_access_token, authenticate_user


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)


bycrypt_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,create_user_request: RequestUser):
    create_user_model = User(username = create_user_request.parameter.username,
                             password = bycrypt_context.hash(create_user_request.parameter.password))
    db.add(create_user_model)
    db.commit()
    

    
@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Could not validate user.")
    token = create_access_token(user.username,user.id,timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}



