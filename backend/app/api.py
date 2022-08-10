from app.schemas.Reservation import ReservationSchema, CancelReservationSchema
from app.schemas.Flight import FlightSchema
import fastapi
import json
from typing import Any
from fastapi import APIRouter, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from loguru import logger
from app import __version__, schemas
from app.config import settings
from app.Utilities import Helper
from app.schemas.Health import Health
from app.controllers import FlightController
from app.schemas.Search import SearchFlightSchema


api_router = APIRouter()


@api_router.get("/health", response_model=Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = Health(name=settings.PROJECT_NAME, api_version=__version__)

    return health.dict()


@api_router.get( "/flight/get-details", response_model = Any, status_code=200)
async def get_flight_details( flight_id: str = Header("")) -> Any:
    """
    get_flight_details
    """
    flight = await FlightController.GetFlightDetails(flight_id =flight_id)
    return flight

@api_router.get( "/reservation/get-details", response_model = Any, status_code=200)
async def get_reservation_details( flight_id: str = Header(""), reservation_id:str = Header("")) -> Any:
    """
    get_reservation_details
    """
    reservation = await FlightController.GetReservationDetails(flight_id = flight_id , reservation_id = reservation_id)
    
    return reservation

@api_router.post( "/reservation/new", response_model = Any, status_code=200)
async def new_reservation(new_reservation:ReservationSchema) -> Any:
    """

    new_reservation

    """
    new_reservation = await FlightController.AddtoReservationQueue(new_reservation) 

    return new_reservation

@api_router.post( "/flights/search", response_model = Any, status_code=200)
async def search_flights(search_criteria:SearchFlightSchema) -> Any:
    """

    search_flights

    """
    search_result = await FlightController.SearchFlights(search_criteria) 

    return search_result

@api_router.post( "/reservation/cancel", response_model = Any, status_code=200)
async def cancel_reservation(cancel_reservation:CancelReservationSchema) -> Any:
    """

    cancel_reservation

    """
    cancel_reservation = await FlightController.CancelReservation(cancel_reservation) 

    return cancel_reservation


@api_router.post( "/flight/new", response_model = Any, status_code=200)
async def add_new_flight(new_flight: FlightSchema) -> Any:
    """
    add_new_flight
    """
    new_flight = await FlightController.AddNewFlight(new_flight = new_flight)
    return new_flight







    

