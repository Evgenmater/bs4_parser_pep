import multiprocessing
from random import shuffle

def bogosort(data, process):
    attempt = 1
    while not sorted(data) == data:
        attempt += 1
        shuffle(data)
    print(f'{process} закончил сортировку. Результат: {data}. Количество '
          f'итераций {attempt}.')


if __name__ == '__main__':

    a = [8, 6, 1, 9, 3]
    b = [8, 6, 1, 9, 3]

    process1 = multiprocessing.Process(target=bogosort, args=(a, 'process1'))
    process2 = multiprocessing.Process(target=bogosort, args=(b, 'process2'))
    process2.start()
    process1.start()