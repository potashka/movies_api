from typing import List
from fastapi import APIRouter, Depends, Query

from src.models.genre import Genre
from src.services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get("/", response_model=List[Genre])
async def genres_list(
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    genre_service: GenreService = Depends(get_genre_service),
):
    return await genre_service.list(page_size=page_size, page_number=page_number)


@router.get("/search", response_model=List[Genre])
async def genres_search(
    query: str,
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    genre_service: GenreService = Depends(get_genre_service),
):
    return await genre_service.search(query=query, page_size=page_size, page_number=page_number)


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)):
    return await genre_service.get_by_id(genre_id)
