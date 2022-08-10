from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

class SearchFlightSchema(BaseModel):
    departure_city:str = ""
    arrival_city:str = ""
    departure_date:str = ""

    def ConstructSearchPhrase(self):
        search_phrase = f"{self.departure_city}|{self.arrival_city}|{self.departure_date[:11]}" 
        search_phrase = search_phrase.upper()
        return search_phrase    

