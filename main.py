import threading
import time
from fastapi import  FastAPI # type: ignore
import uvicorn # type: ignore
from router.hotel import router as hotels_router 
import sys
app = FastAPI()


def cpu_task():
    start = time.time()
    x = 0
    # бесконечный счётчик, пока не пройдёт ~10 секунд
    while time.time() - start < 10:
        for i in range(10_000_000):
            x += i  # чисто CPU-операции
    return x

@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")

    start_time = time.time()
    cpu_task()
    end_time = time.time()
    print(f"Задача CPU завершена за {end_time - start_time:.2f} секунд")

    print(f"\033[31m sync. Начал {id}: {time.time()}\033[0m")

   

    print(sys.getswitchinterval()) 

    time.sleep(10)
    print(f"\033[34m sync. Закончил {id}: {time.time()}")



app.include_router(hotels_router)


# поумолчанию в unicorn - 40 потоков, + reload=False нужно ставить.
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)




