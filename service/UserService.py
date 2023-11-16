from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from model.User import User
from datetime import timedelta,datetime
from typing import Annotated
from fastapi import Depends, HTTPException
from config.config import sessionLocal
from jose import jwt,JWTError
from starlette import status

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = '4a4e0a14fb014a0abbbd4fb72c8dfd72'
ALGORITH = 'HS256'
db_dependency = Annotated[Session,Depends(get_db)]
bycrypt_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# get users
def get_users(db: Session):
    db.query(User).all()
    
    
def get_User_by_id (user_id: int, db: Session):
    db.query(User).filter(user_id == User.id).first()
    
    
    
def authenticate_user(username: str, password: str,db: db_dependency):
    _user = db.query(User).filter(User.username == username).first()
    if not _user:
        return False
    if not bycrypt_context.verify(password, _user.password):
        return False
    return _user
    
    
def create_access_token(username: str,user_id: int, expires_delta: timedelta):
    encode = {'sub': username,'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY, algorithm=ALGORITH)

async def get_current_user(token: Annotated[str,Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Could not validate user.")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="could not validate user")