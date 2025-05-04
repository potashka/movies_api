from typing import List
from fastapi import APIRouter, Depends, Query

from models.person import Person
from services.person import PersonService, get_person_service

router = APIRouter()

@router.get("/", response_model=List[Person])
async def persons_list(
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    person_service: PersonService = Depends(get_person_service),
):
    return await person_service.list(page_size=page_size, page_number=page_number)

@router.get("/search", response_model=List[Person])
async def persons_search(
    query: str,
    page_size: int = Query(50, ge=1, le=100),
    page_number: int = Query(1, ge=1),
    person_service: PersonService = Depends(get_person_service),
):
    return await person_service.search(query=query, page_size=page_size, page_number=page_number)

@router.get("/{person_id}", response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)):
    return await person_service.get_by_id(person_id)
