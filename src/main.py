#!/usr/bin/env python3
from fastapi import FastAPI
from api.database import Base, engine
from api.routes import *
from utils.database import Base, engine

Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
