import app.controllers.FlightController as fc
from app.controllers.SeatConfigurationController import SeatConfigurationManager
from app.database.inmemory import FlightDB
from app.schemas.Passenger import PassengerSchema
from app.schemas.Reservation import ReservationSchema
from app.Utilities import Constants


def main():
    fdb = FlightDB.PopulateFlightsConfiguration()
    nr1 = ReservationSchema(
        flight_id="IC101",
        reservation_id="R1",
        reservation_date="2022-07-25",
        Passengers=[
            PassengerSchema(passenger_id="P1", passenger_name="aarthi"),
            PassengerSchema(passenger_id="P2", passenger_name="pinki"),
            PassengerSchema(passenger_id="P3", passenger_name="maya"),
        ],
    )
    nr2 = ReservationSchema(
        flight_id="IC101",
        reservation_id="R2",
        reservation_date="2022-07-25",
        Passengers=[
            PassengerSchema(passenger_id="P1", passenger_name="ramesh"),
            PassengerSchema(passenger_id="P2", passenger_name="sowmya"),
            PassengerSchema(passenger_id="P3", passenger_name="agathiyan"),
        ],
    )
    fc.AddtoReservationQueue(nr1)
    fc.AddtoReservationQueue(nr2)
    flight_ic101 = fdb.FindFlightById(flight_id="IC101")
    print()
    print("Reservations")
    print()
    print(flight_ic101.reservations)
    print()
    fc.CancelReservation("IC101", "R2")
    print()
    print("Cancellations")
    print()
    print(flight_ic101.cancellations)


main()
