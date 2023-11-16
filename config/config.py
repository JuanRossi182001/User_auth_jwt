from sqlalchemy import create_engine # create_engine es lo q me permite conectarme a la DB
from sqlalchemy.orm import sessionmaker # sessionmaker proporciona una interfaz para interactuar con ella de manera transaccional.
from sqlalchemy.ext.declarative import declarative_base # creo clases heredando declarative_base para que en base a las clases me cree las tablas


DATABASE_URL = "postgresql://postgres:holagente56@localhost:5432/User_auth"


engine = create_engine(DATABASE_URL)       #En resumen, estas líneas están configurando una conexión a la base de datos y creando un objeto de sesión que está asociado a ese motor de base de datos. Este objeto de sesión te permitirá realizar operaciones de base de datos de manera transaccional.
sessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
base = declarative_base()