#!/usr/bin/env python3
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
import os

load_dotenv()

db_url: str = os.getenv('DB_URL', '')
print(db_url)
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
