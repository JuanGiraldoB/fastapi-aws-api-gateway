from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .routers import dogs, users
from .database import engine
from .dependencies import get_db, get_token_header

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(dogs.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
