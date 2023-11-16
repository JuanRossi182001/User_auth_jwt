from sqlalchemy import Column,Integer,String
from config.config import base

class User(base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    
    def as_dict(self):
        return{
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
    
    
    