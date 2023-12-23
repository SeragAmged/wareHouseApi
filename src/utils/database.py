from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# DRIVER_NAME = 'ODBC Driver 17 for SQL Server' or the installed virion
DRIVER_NAME = str(os.getenv('DRIVER_NAME'))
# run Select @@SERVERNAME in SQL server MS
SERVER_NAME = str(os.getenv('SERVER_NAME'))
DATABASE_NAME = str(os.getenv('DATABASE_NAME'))
# sa if you r using root in sql server auth
USER_NAME = str(os.getenv('USER_NAME'))
PASSWORD = str(os.getenv('PASSWORD'))

connection_string = f"mssql+pyodbc://{USER_NAME}:{PASSWORD}@{
    SERVER_NAME}/{DATABASE_NAME}?driver={DRIVER_NAME}"

engine = create_engine(connection_string,echo=True)

Session = sessionmaker(bind=engine)
session = Session()

