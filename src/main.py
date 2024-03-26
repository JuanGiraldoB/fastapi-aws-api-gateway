from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import uvicorn
from mangum import Mangum

from api.models import Base
from api.routers import (
    drivers,
    races,
    teams,
)
from api.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drivers.router)
app.include_router(races.router)
app.include_router(teams.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
