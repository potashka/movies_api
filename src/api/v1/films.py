"""
Маршруты `/api/v1/films/*`.
"""
from typing import List

from fastapi import APIRouter, Depends, Query

from src.models.film import Film, ShortFilm
from src.services.film import FilmService, get_film_service

router = APIRouter()


@router.get("/", response_model=List[ShortFilm])
async def films_list(
    sort: str | None = Query(
        None,
        description="Поле сортировки; префикс «-» = по убыванию",
        example="-imdb_rating",
    ),
    genre: str | None = Query(
        None,
        description="Название жанра для фильтра (например «Action»)",
        example="Fantasy",
    ),
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    film_service: FilmService = Depends(get_film_service),
):
    """
    Получить **список фильмов** (короткие карточки).

    Возвращаются только поля, необходимые для плитки: `uuid`, `title`,
    `imdb_rating`, `poster_url`.

    * Сортировка задаётся параметром ``sort``.  
      Пример: ``?sort=-imdb_rating`` — топ‑фильмы по рейтингу.
    * Фильтр по жанру .
    * Пагинация: ``page_size`` и ``page_number``.

    Returns
    -------
    List[ShortFilm]
        Список фильмов текущей страницы.
    """
    return await film_service.list(
        sort=sort, genre=genre, page_size=page_size, page_number=page_number
    )


@router.get("/search", response_model=List[ShortFilm])
async def films_search(
    query: str = Query(
        ...,
        description=(
            "Поисковая строка. Полнотекстовый поиск выполняется сразу по "
            "нескольким полям: название фильма, описание, имена актёров, "
            "режиссёров и сценаристов (fuzziness = auto)."
        ),
        example="Star Wars",
    ),
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    film_service: FilmService = Depends(get_film_service),
) -> List[ShortFilm]:
    """
    Полнотекстовый **поиск фильмов**.

    Ищет одновременно по полям `title`, `description`,
    `actors/directors/writers.full_name`.

    Returns
    -------
    List[ShortFilm]
        Релевантные фильмы (карточки) в порядке score ElasticSearch.
    """
    return await film_service.search(query=query, page_size=page_size, page_number=page_number)


@router.get("/{film_id}", response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)):
    """
    Получить **полную информацию** о фильме по UUID.

    Raises
    ------
    HTTPException(404)
        Если фильм не найден.
    """
    return await film_service.get_by_id(film_id)
