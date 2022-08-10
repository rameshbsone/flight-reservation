from typing import Any
from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from loguru import logger

from app.api import api_router
from app.Utilities import Constants
from app.config import settings, setup_app_logging
import uvicorn
from app.database.inmemory import FlightDB
from app.controllers import FlightController

# setup logging as early as possible
setup_app_logging(config=settings)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

root_router = APIRouter()



@root_router.get("/")
async def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


def run():
    """
    This function to run configured uvicorn server.
    """
    uvicorn.run(app, host="localhost", port=Constants.API_PORT, log_level="debug")




def main():
    logger.warning("Running in development mode. Do not run like this in production.")
    FlightDB.PopulateFlightsConfiguration()
 #   FlightController.PopulateReservations()
    run()




if __name__ == "__main__":
    main()
    # Use this for debugging purposes only
