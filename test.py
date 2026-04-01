# import asyncio

# async def handler():
#     print('handler')
#     await asyncio.sleep(11)
#     print('handler done')


# async def main():
#     print('main')
#     res = handler() 
#     print('res', res)


#     await res

# asyncio.run(main())


# def test():
#     print('test')

# test()
# !!!

# import threading
# import time

# counter = 0

# def increment():
#     global counter
#     for _ in range(10000000):
#         counter += 1

# t1 = threading.Thread(target=increment)
# t2 = threading.Thread(target=increment)
# t3 = threading.Thread(target=increment)

# t1.start()
# t2.start()
# t3.start()

# t1.join() #ждем поток
# t2.join()
# t3.join()
# print(counter)
# threading.main_thread().setName('mazaka-main')
# print(threading.main_thread())


# потоки существуют внутри процессов 



import threading
import time
import tkinter as tk
import ctypes


#* kernel 
kernel32 = ctypes.WinDLL('kernel32')
pid = kernel32.GetCurrentProcessId()
print(f"PID текущего процесса: {pid}")

# Пример: вызов функции Beep(frequency, duration)
kernel32.Beep(750, 300)  # издаёт звук частотой 750 Hz, 300 мс

#* kernel end 

root = tk.Tk()

def long_task():
    time.sleep(5)
    print("Task done")

threading.Thread(target=long_task).start()  # не блокируем GUI

root.title("Пример GUI")

tk.Label(root, text="Введите имя:").pack()
entry = tk.Entry(root)
entry.pack()

def greet():
    print("Привет,", entry.get())

tk.Button(root, text="Сказать привет", command=greet).pack()

root.mainloop()

