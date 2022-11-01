"""Current weather report model"""

from typing import Tuple, Optional
from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field


# class WeatherSchema(BaseModel):
#     city: Optional[Indexed(str, unique=True)]
#     coordinates: Optional[Tuple[float, float]]
#     description: Optional[str] = Field(...)
#     temperature: Optional[float] = Field(...)
#     humidity: Optional[float]
#     wind_speed: Optional[float]
#     sky: Optional[str]
#     time:  Optional[datetime]
#     sunrise: Optional[datetime]
#     sunset: Optional[datetime]

class WeatherSchema(BaseModel):
    city: Indexed(str, unique=True)
    coordinates: Tuple[float, float]
    description: str = Field(...)
    temperature: float = Field(...)
    humidity: float
    wind_speed: float
    time: datetime
    sunrise: Optional[datetime]
    sunset: Optional[datetime]


class WeatherReport(Document, WeatherSchema):
    """Weather report DB representation"""

    def __repr__(self) -> str:
        return f"<WeatherReport {self.city}>"

    def __str__(self) -> str:
        return self.city

    def __hash__(self) -> int:
        return hash(self.city)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, WeatherReport):
            return self.city == other.city
        return False

    @property
    def created(self) -> datetime:
        """Datetime weather report was created from ID"""
        return self.id.generation_time

    @classmethod
    async def by_city(cls, city: str) -> "WeatherReport":
        """Get a weather report by city"""
        return await cls.find_one(cls.city == city)


__beanie_models__ = [WeatherReport]
