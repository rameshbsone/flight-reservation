from typing import Any, List, Optional

from pydantic import BaseModel

from app.schemas.Passenger import PassengerSchema
from app.Utilities import Constants


class ReservationSchema(BaseModel):
    flight_id: str = ""
    reservation_id: str = ""
    reservation_date: str = ""
    cancellation_date: str = ""
    reservation_status: str = Constants.RESERVATION_NEW
    Passengers: List[PassengerSchema] = []


class CancelReservationSchema(BaseModel):
    flight_id: str = ""
    reservation_id: str = ""
    passenger_id: str = ""
