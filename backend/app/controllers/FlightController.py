from app.database.inmemory.FlightDB import flightmaster
from app.schemas.Reservation import ReservationSchema
from app.Utilities import Helper
from app.schemas.Reservation import ReservationSchema
from app.schemas.Passenger import PassengerSchema
from app.schemas.Flight import FlightCollection
from app.schemas.Reservation import CancelReservationSchema
from app.schemas.Flight import FlightSchema
from loguru import logger
from app.schemas.Search import SearchFlightSchema



async def AddtoReservationQueue(new_reservation: ReservationSchema):    
    if len(new_reservation.flight_id) > 0:
        flight = flightmaster.FindFlightById(flight_id=new_reservation.flight_id)
        if flight:
            new_reservation.reservation_id = "R-" + Helper.CurrentDateTime("%Y%m%d-%H%M%S")
            passenger_ctr = 1
            for passenger in new_reservation.Passengers:
                passenger.passenger_id = f"P-{passenger_ctr}"
                passenger_ctr = passenger_ctr + 1
            flight.AddToQueue(new_reservation)
            flight.ProcessReservations()
            new_reservation = flight.FindReservation(new_reservation.reservation_id)
    return new_reservation.dict()       


async def CancelReservation(cancel_reservation:CancelReservationSchema):
    flight = flightmaster.FindFlightById(flight_id = cancel_reservation.flight_id)
    if flight:
        flight.CancelReservation(reservation_id = cancel_reservation.reservation_id)
    cancel_reservation = await GetReservationDetails(flight_id = cancel_reservation.flight_id,reservation_id = cancel_reservation.reservation_id)
    return cancel_reservation 

async def GetFlightDetails(flight_id: str):
    flight = flightmaster.FindFlightById(flight_id = flight_id) 
    if (flight == None):
        Helper.RaiseHttpException(code = 400 ,  message = f"Flight {flight_id} not found" , source = "FlightController.GetFlightDetails ", data = None)
    return flight.dict() 

async def GetReservationDetails(flight_id:str,reservation_id:str):
    reservation = None
    flight = flightmaster.FindFlightById(flight_id = flight_id)
    if flight:
        reservation = flight.FindReservation(reservation_id = reservation_id)
        if (reservation == None): Helper.RaiseHttpException(code = 400,message = f"reservation:{reservation_id} not found for flight: {flight_id}", source ="FlightController.GetReservationDetails", data = None)
    else:
        Helper.RaiseHttpException(code = 400 ,  message = f"Flight {flight_id} not found" , source = "FlightController.GetReservationDetails", data = None)
    return reservation.dict()


def PopulateReservations():
    nr1 = ReservationSchema(flight_id="IC101",reservation_id="R1",reservation_date="2022-07-25", Passengers=[PassengerSchema(passenger_id="P1", passenger_name="aarthi"),PassengerSchema(passenger_id="P2", passenger_name="pinki"),
    PassengerSchema(passenger_id="P3", passenger_name="maya")])
    nr2 = ReservationSchema(flight_id="IC101",reservation_id="R2",reservation_date="2022-07-25",Passengers=[PassengerSchema(passenger_id="P1", passenger_name="ramesh"),PassengerSchema(passenger_id="P2", passenger_name="sowmya"),PassengerSchema(passenger_id="P3", passenger_name="agathiyan")])
    AddtoReservationQueue(nr1)
    AddtoReservationQueue(nr2)

async def SearchFlights(search_fields:SearchFlightSchema):
    search_result: FlightCollection = FlightCollection()
    for flight in flightmaster.Flights:
        if flight.ConstructSearchPhrase() == search_fields.ConstructSearchPhrase():
            search_result.Flights.append(flight)
    return search_result.dict()  

async def AddNewFlight(new_flight:FlightSchema):
    flightmaster.AddFlight(new_flight)
    new_flight = await GetFlightDetails(flight_id = new_flight.flight_id)
    return new_flight



        


