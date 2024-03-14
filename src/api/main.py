from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from mangum import Mangum

from api.models import Base
from api.routers import dogs, users
from api.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(dogs.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

handler = Mangum(app)
