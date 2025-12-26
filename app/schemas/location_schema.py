from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional, Any


class Location(BaseModel):
    """
    Represents a geographic location.
    
    Attributes:
        country (str): The name of the country.
        region (str): The name of the region within the country.
        province (Optional[str]): The name of the province, if applicable.
        city (str): The name of the city.
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.
    """

    country: str
    region: str
    province: Optional[str]
    city: Optional[str]
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class IncidentDate(BaseModel):
    """
    Represents the date of an incident.
    
    Attributes:
        year (int): The year of the incident.
        month (int): The month of the incident (1-12).
        day (Optional[int]): The day of the incident (1-31), optional if only year and month are known.
    """

    year: int
    month: int
    day: Optional[int]

    class Config:
        from_attributes = True


class Incident(BaseModel):
    """
    Incident model representing a recorded attack incident.

    Attributes:
        year (int): The year the incident occurred.
        month (int): The month the incident occurred (1-12).
        date: A nested model representing the date the incident occurred.
        attack_type (str): The type of attack (e.g., bombing, shooting).
        target (str): The target of the attack (e.g., civilian, military).
        suicide_bombing (bool): Indicates whether the attack involved a suicide bombing.
    
    Config:
        from_attributes (bool): Allows the model to be created from attributes.
    """

    date: IncidentDate
    description: Optional[str]
    attack_type: str
    target: str
    suicide_bombing: bool

    class Config:
        from_attributes = True
    

    @model_validator(mode="before")
    @classmethod
    def wrap_flat_fields(cls, data: Any) -> Any:
        # Check if the data is a SQLAlchemy model (has an __dict__) 
        # or a dictionary from the DB and wrap fields
        if hasattr(data, "__dict__"):
            row = data.__dict__
        else:
            row = data

        # Wrap the flat fields into the nested keys the schema expects
        return {
            "date": row,
            "description": row.get("description"),
            "attack_type": row.get("attack_type"),
            "target": row.get("target"),
            "suicide_bombing": row.get("suicide_bombing"),
        }



class CreateLocation(Location, Incident):
    """
    CreateLocationthat combines the attributes of Location and Incident classes.
    This model is used to represent a location associated with a specific incident, ensuring that
    the data adheres to the validation rules defined in the parent classes.

    Attributes:
        - Inherits all attributes from Location and Incident classes.
    """

    pass


class LocationResponse(BaseModel):
    """
    LocationResponse is a Pydantic model that represents the response structure for a location-related API.
    
    Attributes:
        id (int): The unique identifier for the location.
        date_created (datetime): The timestamp when the location was created.
        location (Location): A nested model representing the geographical details of the location.
        incident (Incident): A nested model representing the incident associated with the location.
    
    Config:
        from_attributes (bool): Enables the model to accept attributes from the ORM model.
    """

    id: int
    date_created: datetime
    date_updated: datetime
    location: Location
    incident: Incident

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def wrap_flat_fields(cls, data: Any) -> Any:
        # Check if the data is a SQLAlchemy model (has an __dict__) 
        # or a dictionary from the DB and wrap fields
        if hasattr(data, "__dict__"):
            row = data.__dict__
        else:
            row = data

        # Wrap the flat fields into the nested keys the schema expects
        return {
            "id": row.get("id"),
            "date_created": row.get("date_created"),
            "date_updated": row.get("date_updated"),
            "location": row,  # Pydantic will extract relevant fields for Location
            "incident": row,  # Pydantic will extract relevant fields for Incident
        }
