from app.schemas.SeatingConfiguration import (
    BlockSchema,
    RowCollection,
    RowSchema,
    SeatSchema,
)

from app.schemas.Flight import ConfigurationSchema, FlightCollection, FlightSchema

flightmaster = FlightCollection()


def PopulateFlightsConfiguration() -> FlightCollection:
    flightmaster.AddFlight(FlightSchema(
                            flight_id="BA101-1",
                            flight_no="BA101", 
                            flight_name="britishairways", 
                            departure_city="london", 
                            arrival_city="chennai",
                            departure_date="2022-08-01 01:30:00", 
                            arrival_date="2022-08-01 14:00:00",
        configuration=ConfigurationSchema(no_of_rows=2, blocks_per_row=3, seats_per_block=[1, 1, 1])            
    ))
    flightmaster.AddFlight(FlightSchema(
                            flight_id="SA102-1",
                            flight_no="SA102",
                            flight_name="singaporeairlines",
                            departure_city="chennai",
                            arrival_city="singapore",
                            departure_date="2022-08-01 03:15:00",
                            arrival_date="2022-08-01 09:30:00",
        configuration=ConfigurationSchema(no_of_rows=1, blocks_per_row=3, seats_per_block=[3, 3, 3])
    ))
    return flightmaster


