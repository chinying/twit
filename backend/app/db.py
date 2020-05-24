import os

import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# TODO: fail if not exists
DB_URI = os.getenv("DB_URI")

db = databases.Database(DB_URI)

engine = create_engine(DB_URI,)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
