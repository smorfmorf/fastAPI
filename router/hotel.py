from turtle import title

from fastapi import APIRouter, Body, FastAPI, Query, Depends
from typing import Annotated

from sqlalchemy import insert, select
from models.hotels import HotelsOrm
from pydantic import BaseModel, Field

from database import async_session_maker

import threading
print('кол-во потоков: ', threading.active_count())


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

hotels = [
    {"id": 1, "location": "Отель 1"},
    {"id": 2, "location": "Отель 2"},
    {"id": 3, "location": "Отель 3"},
    {"id": 4, "location": "Отель 4"},
]

#! Depends - протаскивает переменные из pydantic схем в Query параметры 
class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1)]
    limit: Annotated[int | None, Query(None, ge=1, lt=100)]

PaginationDep = Annotated[PaginationParams, Depends()]



@router.get("",  summary = "Получить список отелей",description="Получить список",)
async def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="id item")
):
    # if id:
    #     # ["первый hotel - что положить в новый []" обычный цикл for <переменная> in <итерируемый объект> if <условие>]
    #     return [hotel for hotel in hotels if hotel["id"] == id]
    # if pagination.page and pagination.limit: 
    #     # 1 срез возьми все отели начиная с нужной стр, 2-ой срез возьми нужное кол-во
    #     return hotels[pagination.limit * (pagination.page - 1):][:pagination.limit]
    # else: 
    #     return hotels
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)

        hotels = result.all()
        
        print(hotels)

        return hotels




#! схема валидации - библиотека pydantic
class Hotel(BaseModel):
    title: str | None = Field(None) #типо Body
    location: str | None = Field(None)

@router.post('')
# body - ждет ключ значение из-за embed
async def create_hotel(hotel: Hotel = Body(
    openapi_examples={
    "1": {"value": {"location": "666", "title": "Отель 666Sik"}}, 
    "2": {"value": {"location": "777", "title": "Отель 777Sik"}}
    })):
    
    # global hotels
    # hotels.append({
    #     "id": len(hotels) + 1,
    #     "name": hotel.name
    # })
    async with async_session_maker() as session:
        # раскрываем словарь **
        add_hotel_stmt = insert(HotelsOrm).values(**hotel.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    print({"message": 'ok'})
    return hotels



@router.delete('/{id}', summary='Удалить отель по id')
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"message": 'ok'}




@router.put('/{id}')
def update_hotel(id: int, name: str = Body(embed=True)):
    global hotels
    UPDATE_hotel = [hotel for hotel in hotels if hotel["id"] == id][0]
    print(UPDATE_hotel)
    # ⚠️ В Python переменная хранит ссылку на объект. Когда ты пишешь hotel = {...}, ты просто меняешь локальную переменную, а не объект внутри списка.
    # UPDATE_hotel = {"test":name}
    UPDATE_hotel["name"] = name
    return hotels

