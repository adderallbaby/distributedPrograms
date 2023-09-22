import multiprocessing
import time
import random
from multiprocessing import Process


def mulmat(m1, m2, size, divisor, l, queue):
    result = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        result.append(row)

    col = l * (size // divisor)
    row = 0
    if col >= size:
        row = (col // size) * (size // divisor)
        col = col % size
    for i in range(int(size // divisor)):
        for j in range(int(size // divisor)):
            for k in range(int(size)):
                result[i + row][j + col] += m1[i + row][k] * m2[k][j + col]

    queue.put(result)


def work(m1, m2, size, divisor):
    result1 = []
    result2 = []
    result3 = []
    threads = []
    matrixes = []

    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        result1.append(row)

    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        result2.append(row)

    for i in range(size):
        row = []
        for j in range(size):
            row.append(0)
        result3.append(row)

    start = time.time()
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result1[i][j] += m1[i][k] * m2[k][j]
    end = time.time()

    time1 = end - start

    start = time.time()
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result2[j][i] += m1[j][k] * m2[k][i]
    end = time.time()

    time2 = end - start

    start = time.time()

    queue = multiprocessing.Queue()

    for i in range(divisor*divisor):
        threads.append(Process(target=mulmat, args=(m1, m2, size, divisor, i, queue)))

    for i in range(divisor*divisor):
        threads[i].start()

    for i in range(divisor*divisor):
        matrixes.append(queue.get())
        threads[i].join()

    end = time.time()

    time3 = end - start

    for i in range(size):
        for j in range(size):
            for k in range(divisor*divisor):
                result3[i][j] += matrixes[k][i][j]

    if result1 == result3 and result1 == result2:
        print("\ngood", divisor)
    else:
        print("\nbad")

    print(time1)
    print(time2)
    print(time3, "\n\n")


def main():
    size = 200 
    divisor = 4

    m1 = []
    m2 = []

    for i in range(size):
        row = []
        for j in range(size):
            row.append(random.randint(1, 9))
        m1.append(row)

    for j in range(size):
        row = []

        for i in range(size):
            row.append(random.randint(1, 9))
        m2.append(row)

    work(m1, m2, size, 2)
    work(m1, m2, size, 4)
    work(m1, m2, size, 5)
    work(m1, m2, size, 8)

   

if __name__ == '__main__':
    main()
