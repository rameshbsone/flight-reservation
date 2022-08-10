from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

from app.schemas.Reservation import ReservationSchema
from app.schemas.SeatingConfiguration import (
    BlockSchema,
    RowCollection,
    RowSchema,
    SeatSchema,
)
from app.Utilities import Constants, Helper
from loguru import logger


class ConfigurationSchema(BaseModel):
    no_of_rows: int = 3
    blocks_per_row: int = 4
    seats_per_block: List[int] = [3,2,3,3]


class FlightSchema(BaseModel):
    flight_id: str = ""
    flight_no:str = ""
    flight_name:str = ""
    departure_city:str = ""
    arrival_city:str = ""
    departure_date:str = ""
    arrival_date:str = ""
    configuration: ConfigurationSchema = ConfigurationSchema()
    seat_collection: RowCollection = RowCollection()
    queue: List[ReservationSchema] = []
    reservations: List[ReservationSchema] = []
    waiting_list: List[ReservationSchema] = []
    cancellations: List[ReservationSchema] = []



    def ConfigureSeats(self):
        self.seat_collection = self.GetFlightSeating()
        self.AssignSeatNumbers()

    def AssignSeatNumbers(self):
        row_ctr = 0
        for row in self.seat_collection.rows:
            row_ctr = row_ctr + 1            
            seat_letter = 65
            for block in row.blocks:
                for seat in block.seats:                    
                    seat.seat_no = f"{row_ctr}{chr(seat_letter)}"
                    seat_letter = seat_letter + 1
                    if seat.seat_type == Constants.SEAT_WINDOW: seat.seat_no = seat.seat_no +  "(Window) "
            

    def GetFlightSeating(self) -> RowCollection:
        rc = RowCollection()
        for row_ctr in range(0, self.configuration.no_of_rows):
            row = RowSchema()
            for block_ctr in range(0, self.configuration.blocks_per_row):
                block = BlockSchema()
                block.AddSeats(
                    row=row_ctr,
                    block=block_ctr,
                    total_seats=self.configuration.seats_per_block[block_ctr],
                    total_blocks=self.configuration.blocks_per_row,
                )
                row.blocks.append(block)
            rc.rows.append(row)
        return rc

    def AddToQueue(self, new_reservation: ReservationSchema):
        self.queue.append(new_reservation)

    def GetVacantSeats(self):
        vacant_seats: List[SeatSchema] = []
        aisle_seats: List[SeatSchema] = []
        window_seats: List[SeatSchema] = []
        middle_seats: List[SeatSchema] = []

        for row in self.seat_collection.rows:
            for block in row.blocks:
                for seat in block.seats:
                    if seat.seat_status == Constants.SEAT_VACANT:
                        if seat.seat_type == Constants.SEAT_AISLE:
                            aisle_seats.append(seat)
                        if seat.seat_type == Constants.SEAT_WINDOW:
                            window_seats.append(seat)
                        if seat.seat_type == Constants.SEAT_MIDDLE:
                            middle_seats.append(seat)
        vacant_seats = aisle_seats + window_seats + middle_seats

        return vacant_seats

    def ProcessReservations(self):
        self.AllocateSeats(self.waiting_list, move_to_wait_list=False)
        self.AllocateSeats(self.queue)

    def AllocateSeats(self, reservation_queue: List[ReservationSchema], move_to_wait_list: bool = True):
        for new_reservation in reservation_queue:
            vacant_seats = self.GetVacantSeats()
            if len(new_reservation.Passengers) <= len(vacant_seats):
                new_reservation.reservation_status = Constants.RESERVATION_CONFIRMED
                new_reservation.reservation_date = Helper.CurrentDateTime()
                for passenger_ctr in range(0, len(new_reservation.Passengers)):
                    #new_reservation.Passengers[passenger_ctr].seat_id = vacant_seats[passenger_ctr].seat_id
                    new_reservation.Passengers[passenger_ctr].Allocate(vacant_seats[passenger_ctr])


                    #new_reservation.Passengers[passenger_ctr].seat = vacant_seats[passenger_ctr]
                    #vacant_seats[passenger_ctr].Allocate()
                self.reservations.append(new_reservation.copy())
                reservation_queue.pop(0)
            else:
                if move_to_wait_list:
                    new_reservation.reservation_status = Constants.RESERVATION_WAITING_LIST
                    self.waiting_list.append(new_reservation.copy())
                    reservation_queue.pop(0)

    def FindSeat(self, seat_id: str):
        seat = None
        arr_seat = seat_id.split("-")
        if len(arr_seat) == 3:
            row_no = int(arr_seat[0])
            block_no = int(arr_seat[1])
            seat_no = int(arr_seat[2])
            seat = self.seat_collection.rows[row_no].blocks[block_no].seats[seat_no]
        return seat

    def __FindReservation(self,reservation_queue:List[ReservationSchema], reservation_id):
        reservation = None
        for resv in reservation_queue:
            if resv.reservation_id == reservation_id:
                reservation = resv
                break
        return reservation    


    def FindReservation(self, reservation_id: str):
        reservation = self.__FindReservation(self.reservations,reservation_id)
        if  reservation == None: reservation = self.__FindReservation(self.waiting_list,reservation_id)
        if reservation == None: reservation = self.__FindReservation(self.cancellations,reservation_id)
        return reservation

    def CancelReservation(self, reservation_id: str):
        if len(reservation_id) > 0:
            reservation = self.FindReservation(reservation_id)

            if reservation:
                for passenger in reservation.Passengers:
                    passenger.DeAllocate()
                reservation.reservation_status = Constants.RESERVATION_CANCELLED
                reservation.cancellation_date = Helper.CurrentDateTime()
                self.cancellations.append(reservation.copy())
                self.DeleteReservation(reservation_id)
                self.ProcessReservations()

    def DeleteReservation(self, reservation_id):
        index = 0
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                self.reservations.pop(index)
                break
            index = index + 1

    def ConstructSearchPhrase(self):
        search_phrase = f"{self.departure_city}|{self.arrival_city}|{self.departure_date[0:10]}" 
        search_phrase = search_phrase.upper()
        return search_phrase    



class FlightCollection(BaseModel):
    Flights: List[FlightSchema] = []

    def AddFlight(
        self, new_flight: FlightSchema)-> FlightSchema:
        if new_flight:
            new_flight.ConfigureSeats()
            self.Flights.append(new_flight)
        return new_flight

    def FindFlightById(self, flight_id: str) -> FlightSchema:
        existing_flight = None
        for flight in self.Flights:
            if flight.flight_id == flight_id:
                existing_flight = flight
                break
        return existing_flight

