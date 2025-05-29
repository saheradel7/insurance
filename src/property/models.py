from src.database import Base
from sqlalchemy import Column, Integer,JSON, String, Boolean, Date, event,Float, ForeignKey
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid
from sqlalchemy.orm import Mapped, relationship

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    index_str = Column(String, unique=True, nullable=False, default= lambda: str(uuid.uuid4()))
    property_value = Column(Float, nullable=False)
    purchase_date = Column(Date)
    year_built = Column(Integer)
    location = Column(String) 
    construction_type = Column(String)
    condition = Column(String)
    number_of_floors = Column(Integer)
    fire_protection_class = Column(String, nullable=True)
    security_system = Column(String, nullable=True)
    earthquake_zone = Column(String, nullable=True)
    flood_zone = Column(String, nullable=True)
    plumbing_type = Column(String, nullable= True)
    roof_type = Column(String, nullable= True)
    heating_type = Column(String, nullable= True)
    electrical_system_type = Column(String, nullable= True)
    current_insurance_provider = Column(String, nullable= True)
    crime_risk_score = Column(Float , nullable = True)
    square_footage = Column(Float , nullable = True)
    distance_to_hydrant_km = Column(Float , nullable = True)
    distance_to_fire_station_km = Column(Float , nullable = True)
    has_swimming_pool = Column(Boolean , default = False)
    has_garage = Column(Boolean , default = False)
    is_historic_property = Column(Boolean , default = False)
    pictures = Column(JSON, nullable=True)
    quotes: Mapped[list["Quote"]] = relationship(
        "Quote",
        back_populates="property",
        cascade="all, delete-orphan",
    )

@event.listens_for(Property, "before_insert")
def validate_number_of_floors(mapper, connection, target):
    if  target.number_of_floors < 0:
        raise ValueError("number of floors cant be less than 0")
    if  target.number_of_floors > 100:
        raise ValueError("number of floors cant be more than 100")

class PropertyRequest(BaseModel):
    index_str: str
    property_value: float
    purchase_date: date
    year_built: int
    location: str
    construction_type: str
    condition: str
    number_of_floors: int
    fire_protection_class: Optional[str] = None
    security_system: Optional[str] = None
    earthquake_zone: Optional[str] = None
    flood_zone: Optional[str] = None
    crime_risk_score: Optional[float] = None
    plumbing_type: Optional[str] = None
    square_footage: Optional[float] = None
    roof_type: Optional[str] = None
    has_swimming_pool: Optional[bool] = None
    has_garage: Optional[bool] = None
    heating_type: Optional[str] = None
    electrical_system_type: Optional[str] = None
    distance_to_fire_station_km: Optional[float] = None
    distance_to_hydrant_km: Optional[float] = None
    is_historic_property: Optional[bool] = None
    current_insurance_provider: Optional[str] = None
    pictures: Optional[List[str]] = None

    class Config:
        orm_mode = True
