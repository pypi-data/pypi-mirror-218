# Python -- v3.6

import multiprocessing
import time
import random

class FixedData(object):
    pass


def worker(line, fixed_data):
    t = 0
    print(f'. worker {line} running....')
    time.sleep(random.randint(0,5))
    print(f'. worker {line} done.')
    return t


fixed_data = None


def initializer(init_data):
    global fixed_data
    fixed_data = init_data


def builtin_pool_worker_wrapper(line):
    return worker(line, fixed_data)



def builtin_pool():
    start_time = time.time()
    fixed_data = FixedData()
    with multiprocessing.Pool(4, initializer, (fixed_data,)) as pool:
        lines = [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14),(15,16),(17,18),(19,20)]
        pool.map(builtin_pool_worker_wrapper, lines)
        pool.close()
        pool.join()
        pool.terminate()
    print(f'. endtime {time.time() - start_time}')


if __name__ == '__main__':
    # custom_pool()
    # print(f'. custom_pool complete')
    builtin_pool()
    print(f'. builtin_pool complete')
    print(f'done.')

