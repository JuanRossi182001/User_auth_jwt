from fastapi import FastAPI,Depends,HTTPException
from router import UserRouter
from model import User
from config.config import engine
from starlette import status
from typing import Annotated
from config.config import sessionLocal
from sqlalchemy.orm import Session
from service.UserService import get_current_user

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(UserRouter.router)
User.base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@app.get ("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Authentication failed")
    return {"User": user}
