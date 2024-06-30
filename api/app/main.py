from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .routers import search, users, archive

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app.include_router(archive.router)
app.include_router(search.router)


@app.get("/", tags=['root'])
async def read_root(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    return {"message": "Welcome to Provicia REST API!"}
