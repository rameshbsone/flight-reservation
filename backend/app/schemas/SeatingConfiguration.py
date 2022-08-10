from typing import Any, List, Optional

from pydantic import BaseModel

from app.Utilities import Constants


class SeatSchema(BaseModel):
    seat_id: str = ""
    seat_no: str = ""
    seat_type: str = Constants.SEAT_MIDDLE
    seat_status: str = Constants.SEAT_VACANT

    def Allocate(self):
        self.seat_status = Constants.SEAT_RESERVED

    def DeAllocate(self):
        self.seat_status = Constants.SEAT_VACANT


class BlockSchema(BaseModel):
    seats: List[SeatSchema] = []

    def AddSeats(self, row: int, block: int, total_seats: int, total_blocks: int):

        for seat_ctr in range(0, total_seats):
            seat = SeatSchema(seat_id=f"{row}-{block}-{seat_ctr}")
            if block == 0:
                if seat_ctr == 0:
                    seat.seat_type = Constants.SEAT_WINDOW
                if seat_ctr == total_seats - 1 and seat_ctr > 0:
                    seat.seat_type = Constants.SEAT_AISLE
            if block == total_blocks - 1:
                if seat_ctr == 0:
                    seat.seat_type = Constants.SEAT_AISLE
                if seat_ctr == total_seats - 1:
                    seat.seat_type = Constants.SEAT_WINDOW
            if block > 0 and block < total_blocks - 1:
                if seat_ctr in [0, total_seats - 1]:
                    seat.seat_type = Constants.SEAT_AISLE
            self.seats.append(seat)


class RowSchema(BaseModel):
    blocks: List[BlockSchema] = []


class RowCollection(BaseModel):
    rows: List[RowSchema] = []
