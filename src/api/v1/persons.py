"""Маршруты для работы с персонами (/api/v1/persons/*)."""
from typing import List
from fastapi import APIRouter, Depends, Query

from src.models.person import Person
from src.services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/", response_model=List[Person])
async def persons_list(
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    person_service: PersonService = Depends(get_person_service),
):
    """Список персон с пагинацией.

    Возвращается упорядоченный по фамилии список актёров, режиссёров
    и сценаристов.

    Параметры
    ----------
    page_size : int
        Количество элементов на странице.
    page_number : int
        Номер запрашиваемой страницы.

    Возвращает
    ----------
    list[Person]
        Персоны текущей страницы.
    """
    return await person_service.list(page_size=page_size, page_number=page_number)


@router.get("/search", response_model=List[Person])
async def persons_search(
    query: str,
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    person_service: PersonService = Depends(get_person_service),
):
    """Поиск персон по имени/фамилии.

    Параметры
    ----------
    query : str
        Часть имени, например «Lucas».
    page_size, page_number
        Параметры пагинации.

    Возвращает
    ----------
    list[Person]
        Найденные персоны.
    """
    return await person_service.search(query=query, page_size=page_size, page_number=page_number)


@router.get("/{person_id}", response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)):
    """Подробности персоны по её UUID.

    В ответе также присутствует список фильмов и ролей,
    в которых участвовал данный человек.
    """
    return await person_service.get_by_id(person_id)
