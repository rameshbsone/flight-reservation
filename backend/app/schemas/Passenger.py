from typing import Any, List, Optional

from pydantic import BaseModel

from app.schemas.SeatingConfiguration import SeatSchema
from app.Utilities import Constants
from app.Utilities import Helper
from loguru import logger


class PassengerSchema(BaseModel):
    passenger_id: str = ""
    passenger_name: str = ""
    seat_id: str = ""
    seat_status = "Not Allocated"
    seat_cancelled_date = ""
    seat: SeatSchema = None

    def Allocate(self, seat:SeatSchema):
        self.seat_id = seat.seat_id
        self.seat_status = Constants.PASSENGER_SEAT_ALLOCATED
        self.seat = seat
        self.seat.Allocate()

    def DeAllocate(self):
        self.seat_id = ""
        self.seat_status = Constants.PASSENGER_SEAT_NOT_ALLOCATED
        
        if self.seat:
            self.seat.DeAllocate()
        self.seat = None  
        self.seat_cancelled_date = Helper.CurrentDateTime()      
