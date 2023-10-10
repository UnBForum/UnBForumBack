from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = config('DB_URL')

Engine = create_engine(DB_URL, pool_pre_ping=True)
LocalSession = sessionmaker(bind=Engine)
