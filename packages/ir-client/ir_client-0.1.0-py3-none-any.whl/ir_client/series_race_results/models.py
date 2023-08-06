from pydantic import BaseModel, Field
from datetime import datetime


class SeriesRaceResult(BaseModel):
    subsession_id: int


class SeriesRaceResultsSlot(BaseModel):
    results: list[SeriesRaceResult] = Field(default_factory=list)


class SeriesRaceResultCollection(BaseModel):
    slots: dict[datetime, SeriesRaceResultsSlot]
