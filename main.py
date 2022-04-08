# --------------------------
# USER-INTERFACE
# --------------------------

# IMPORTS
from time import time
from threading import Thread
from random import randint, shuffle
from matplotlib import pyplot as plt

from sorting_algorithms import *

# HOW TO:
# LENGTH determines the length of the array to be sorted.
# LOOP determines how many times each sorting function is run.
# UPPER/LOWER determines the upper and lower bounds of the elements of the array
#   to be sorted. For example: randint(UPPER, LOWER)
# If COMPARE_FNS and CHANGE_PARAMS are false, SORTFN determines the sorting
#   function to be used and tested.
# If COMPARE_FNS is true, the functions in SORTFNS will be run simultaneously
#   through threading and will print out the result.
# If CHANGE_PARAMS is true, COMPARE_FNS is irrelevant, and it will run the
#   sorting functions in SORTFNS on an array of LENGTH length and increment the
#   variable LENGTH by LENGTH_INCREMENT after sorting LOOP times, until LENGTH
#   is greater than or equal to LENGTH_LIMIT.

# Available algorithms:
# merge_sort;
# radix_sort;
# insertion_sort;
# bubble_sort;

# Parameters - Change at will
LENGTH = 10000
LOOP =1
UPPER = 1e4
LOWER = -UPPER

SORTFN = merge_sort
SORTFNS = [merge_sort, radix_sort]
COMPARE_FNS = True

CHANGE_PARAMS = False
LENGTH_INCREMENT = +1000
LENGTH_LIMIT = 10000


# --------------------------
# Time sorting-function
# --------------------------


def time_sort(sortfn, result, loop=1):
    global LENGTH

    dt = []
    array = [randint(LOWER, UPPER) for _ in range(LENGTH)]

    for i in range(loop):
        start = time()
        sortfn(array)
        stop = time()
        shuffle(array)

        dt.append(stop - start)

    avg = sum(dt) / len(dt)
    if not COMPARE_FNS and not CHANGE_PARAMS:
        print(f"Sorting function: "
              f"{sortfn.__name__}\n"
              f"Array length: "
              f"{LENGTH}\n"
              f"Number of iterations: "
              f"{LOOP}\n"
              f"Upper/Lower data-values: "
              f"{UPPER}/{LOWER}\n"
              f"Average: "
              f"{sum(dt)} s / {len(dt)} \n\t= {avg} s")
    if not CHANGE_PARAMS:
        result[sortfn.__name__] = avg
    elif CHANGE_PARAMS and LENGTH <= LENGTH_LIMIT:
        result.append(tuple((LENGTH, avg)))
        LENGTH += LENGTH_INCREMENT
        time_sort(sortfn, result, loop=LOOP)


def main():
    global LENGTH

    threads, results = list(), dict()

    result = list() if CHANGE_PARAMS else dict()

    if not CHANGE_PARAMS:
        if COMPARE_FNS:
            print(
                f"Array length: {LENGTH}\n"
                f"Number of iterations: {LOOP}\n"
                f"Upper/Lower data-values: {UPPER}/{LOWER}\n"
            )
            for fn in SORTFNS:
                thread = Thread(
                    target=lambda: time_sort(fn, result, loop=LOOP))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            for sortfn, avg in result.items():
                print(sortfn, avg, "s")
        else:
            time_sort(SORTFN, result, loop=LOOP)
    elif CHANGE_PARAMS:
        original_length = LENGTH
        for fn in SORTFNS:
            LENGTH = original_length
            result = []
            time_sort(fn, result, loop=LOOP)
            results[fn.__name__] = result
        for fn, avgs in results.items():
            print(fn, avgs)
            x, y = [], []
            for length, avg in avgs:
                x.append(length)
                y.append(avg)
            plt.plot(x, y, label=fn)
        plt.title("Time taken based on length of array")
        plt.xlabel("Length of array")
        plt.ylabel("Time in seconds")
        plt.legend()
        plt.grid()
        plt.show()


if __name__ == '__main__':
    main()
