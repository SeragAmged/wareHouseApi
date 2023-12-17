#!/usr/bin/env python3
from fastapi import APIRouter

router = APIRouter()

@router.get('/health')

def get_health():
    return {"massgae": "ok"}