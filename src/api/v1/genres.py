"""Маршруты для работы с жанрами (/api/v1/genres/*)."""
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
    """Список всех жанров с пагинацией.

    Возвращает жанры в алфавитном порядке.

    Параметры
    ----------
    page_size : int
        Сколько элементов на страницу.
    page_number : int
        Какая именно страница нужна.

    Возвращает
    ----------
    list[Genre]
        Массив жанров текущей страницы.
    """
    return await genre_service.list(page_size=page_size, page_number=page_number)


@router.get("/search", response_model=List[Genre])
async def genres_search(
    query: str,
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    genre_service: GenreService = Depends(get_genre_service),
):
    """Полнотекстовый поиск жанров по названию.

    Параметры
    ----------
    query : str
        Подстрока, по которой ищем.
    page_size, page_number
        Пагинация.

    Возвращает
    ----------
    list[Genre]
        Найденные жанры.
    """
    return await genre_service.search(query=query, page_size=page_size, page_number=page_number)


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)):
    """Получить жанр по UUID.

    Если жанр не существует, вернётся HTTP 404.
    """
    return await genre_service.get_by_id(genre_id)
