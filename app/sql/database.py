from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os,sys
from config import make_conf_dict

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


conf=make_conf_dict()

engine = create_engine(f"mysql+mysqlconnector://{conf.user}:{conf.password}@{conf.host}:{conf.port}/{conf.database}?charset=utf8")

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()