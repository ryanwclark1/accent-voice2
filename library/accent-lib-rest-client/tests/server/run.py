# Copyright 2023 Accent Communications

import secrets
from pathlib import Path
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()

ROOT = Path(__file__).parent / 'server_data'
USERS: dict[str, str] = {'username': 'password'}

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_valid = secrets.compare_digest(credentials.username, 'username')
    is_password_valid = secrets.compare_digest(credentials.password, 'password')

    if not (is_username_valid and is_password_valid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.get("/auth/{path:path}")
async def auth_route(path: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return await serve_file(path)

@app.get("/{path:path}")
async def main_route(path: str):
    return await serve_file(path)

async def serve_file(path: str):
    file_path = ROOT / path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    with file_path.open('rb') as f:
        content = f.read()

    return JSONResponse(content=content)
