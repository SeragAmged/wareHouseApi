from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

DRIVER_NAME = str(os.getenv('DRIVER_NAME'))#DRIVER_NAME = 'ODBC Driver 17 for SQL Server' or the installed virion
SERVER_NAME = str(os.getenv('SERVER_NAME'))#run Select @@SERVERNAME in SQL server MS
DATABASE_NAME = str(os.getenv('DATABASE_NAME'))
USER_NAME = str(os.getenv('USER_NAME'))#sa if you r using root in sql server auth
PASSWORD = str(os.getenv('PASSWORD'))

connection_string = f"mssql+pyodbc://{USER_NAME}:{PASSWORD}@{
    SERVER_NAME}/{DATABASE_NAME}?driver={DRIVER_NAME}"

engine = create_engine(connection_string)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
