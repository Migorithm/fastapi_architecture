from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./{}.db".format

class ConfigDB:
    def __new__(cls,url):
        cls._engine = create_engine(
            SQLALCHEMY_DATABASE_URL(url),
            connect_args={"check_same_thread":False}
        )
        cls._base = declarative_base()
        return cls
    
    @classmethod #Dependency
    def get_db(cls):
        
        cls._SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind= cls._engine
        )
        db = cls._SessionLocal()

        try :
            yield db #Actual return is generator but when it is used as dependency, it's altered to Session.

        finally:
            db.close()
        
        """
        # @app.get('/users/',response_model=user)
        # def read_users(skip:int=0, limit:int=100, db:Session = Depends(DEV.get_db)): #####
        #     user = get_users(db,skip=skip,limit=limit)
        #     return user
        """
        
    @classmethod
    def create_tables(cls):
        cls._base.metadata.create_all(bind=cls._engine)
        
        
class DevDB(ConfigDB):
    def __new__(cls):
        return super(DevDB,cls).__new__(cls,"dev")

class TestDB(ConfigDB):
    def __new__(cls):
        return super(TestDB,cls).__new__(cls,"test")
        
class ProdDB(ConfigDB):
    def __new__(cls):
        return super(ProdDB,cls).__new__(cls,"prod")


db = {
    "dev" : DevDB(),
    "test" : TestDB(),
    "prod" : ProdDB()
}








# DEV:DevDB = db.get("dev")
# from sqlalchemy import Boolean, Column, Integer, String



# class User(DEV._base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
    
# DEV.create_tables()
# from fastapi import FastAPI,Depends

# from pydantic import BaseModel

# class user(BaseModel):
#     id :int
#     email : str
#     hashed_password : str
#     is_active : bool
    
# app = FastAPI()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).first()

# @app.get('/users/',response_model=user)
# def read_users(skip:int=0, limit:int=100, db:Session = Depends(DEV.get_db)):
#     user = get_users(db,skip=skip,limit=limit)
#     return user







 



    
    




