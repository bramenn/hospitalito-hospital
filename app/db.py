from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import POSTGRES_URI

conn = create_engine(POSTGRES_URI)

Session = sessionmaker(bind=conn)

session = Session()
Base = declarative_base()
