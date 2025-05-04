from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException

from src.models.film import Film, ShortFilm
from src.services.film import FilmService, get_film_service

router = APIRouter()

@router.get("/", response_model=List[ShortFilm])
async def films_list(
    sort: str | None = Query(None, description="Sort field, prefix '-' for desc"),
    genre: str | None = Query(None, description="Genre UUID filter"),
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    film_service: FilmService = Depends(get_film_service),
):
    return await film_service.list(sort=sort, genre=genre, page_size=page_size, page_number=page_number)

@router.get("/search", response_model=List[ShortFilm])
async def films_search(
    query: str,
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    film_service: FilmService = Depends(get_film_service),
):
    return await film_service.search(query=query, page_size=page_size, page_number=page_number)

@router.get("/{film_id}", response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)):
    return await film_service.get_by_id(film_id)