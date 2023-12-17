#!/usr/bin/env python3
from fastapi import FastAPI
from api.routes import *


app = FastAPI()

app.include_router(router)

