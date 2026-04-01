import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()  # по умолчанию ищет .env в текущей папке
MY_ENV = os.getenv("MY_VAR")
print(MY_ENV)


class BaseORM(DeclarativeBase):
    pass

engine = create_async_engine("postgresql+asyncpg://postgres:max001195164@localhost:5432/8H", echo=True)  # logging SQL запросов
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False) # - тоже для работы с БД, но в рамках транзакции


async def main():
    # Низкий уровень: чистый SQL
    # async with engine.begin() as conn:  # ← транзакция открывается
    #    res =  await conn.execute(text("SELECT * FROM reports"))  # ← выполняем запрос
    #    print( res.fetchall())  # ← 1, так как была вставлена одна строка

    # Пример 1: сессия для выполнения ORM запросов 
    async with async_session_maker() as session:
        result = await session.execute(text("SELECT * FROM reports"))
        rows = result.fetchall()
        print(rows)

if __name__ == "__main__":
    asyncio.run(main())
