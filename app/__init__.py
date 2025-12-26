from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from app.core.database import close_db, init_db
from app.routers.location import router as location_router
# API version and docs URLs
api_version = "v1"
BASE_URL = f"/api/{api_version}"
swagger_docs_url = f"{BASE_URL}/docs"
redoc_docs_url = f"{BASE_URL}/redoc"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup, initialize the database
    await init_db()

    # yield control to the application
    yield

    # on shutdown, close the db connection
    await close_db()


app = FastAPI(
    lifespan=lifespan,
    title="Uhalifu records API",
    description="This API shows all records of all country attacked by terrorists.",
    swagger_docs_url=swagger_docs_url,
    redoc_docs_url=redoc_docs_url,
    version="1.0.0",
)

# register routers
app.include_router(location_router, prefix=f"{BASE_URL}", tags=["Location"])

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)