from typing import List, Optional
from pydantic import BaseModel, Field


class ShortFilm(BaseModel):
    uuid: str = Field(alias="id")
    title: str
    imdb_rating: Optional[float] = None


class Film(BaseModel):
    uuid: str = Field(alias="id")
    title: str
    imdb_rating: Optional[float] = None
    description: Optional[str]
    genre: List[dict] = []  # [{"uuid": str, "name": str}]
    actors: List[dict] = []
    writers: List[dict] = []
    directors: List[dict] = []
