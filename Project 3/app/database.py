from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL='postgresql://postgres:11092002@localhost/vehicle_routing'

engine=create_engine(SQL_ALCHEMY_DATABASE_URL)
Session_Local=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=Session_Local()
    try:
        yield db
    finally:
        db.close()


