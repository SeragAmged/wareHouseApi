from fastapi import FastAPI
from api.routes import *


app = FastAPI()

app.include_router(router)

