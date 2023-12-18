#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'Serag-pc'
DATABASE_NAME = 'wareHouseMS'
USER_NAME = 'sa'
PASSWORD = '123456789'

connection_string = f"mssql+pyodbc://{USER_NAME}:{PASSWORD}@{
    SERVER_NAME}/{DATABASE_NAME}?driver={DRIVER_NAME}"

engine = create_engine(connection_string, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
