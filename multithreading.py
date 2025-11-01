import threading
import time

def squares():
    for i in range(1, 11):
        print(f'квадрат {i} = {i**2}')

def cubes():
    for i in range(1, 11):
        print(f'куб {i} = {i**3}')

def numbers(n):
    for i in range(1, 11):
        print(f'поток {n}: {i}')
        time.sleep(1)

t1 = threading.Thread(target=squares)
t2 = threading.Thread(target=cubes)
t1.start()
t2.start()
t1.join()
t2.join()
t3 = threading.Thread(target=numbers, args=(1,))
t4 = threading.Thread(target=numbers, args=(2,))
t5 = threading.Thread(target=numbers, args=(3,))
t3.start()
t4.start()
t5.start()
t3.join()
t4.join()
t5.join()