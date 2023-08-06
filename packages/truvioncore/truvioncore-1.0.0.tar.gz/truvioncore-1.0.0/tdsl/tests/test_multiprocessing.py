# Python -- v3.6

import multiprocessing
import time
import random


class Processor(multiprocessing.Process):

    def __init__(self, queue, idx, **kwargs):
        super(Processor, self).__init__()
        self.queue = queue
        self.idx = idx
        self.kwargs = kwargs

    def run(self):
        time.sleep(random.randint(1,3))
        self.queue.put("Process idx={0} is called '{1}'".format(self.idx, self.name))


def worker(varying_data, fixed_data):
    t = 0
    for j in range(1, 10000):
        t += len(varying_data)
    return t


def custom_pool_worker_wrapper(args1, args2, results):
    fixed_data = args1.get()
    args1.task_done()
    while True:
        varying_data = args2.get()
        args2.task_done()
        result = worker(varying_data, fixed_data)
        results.put(result)


def custom_pool():
    iterations = 11
    for i in range(50, 83, 8):
        start_time = time.time()
        fixed_data = [i] * int(pow(10, i/10))
        args1 = multiprocessing.JoinableQueue()
        args2 = multiprocessing.JoinableQueue()
        results = multiprocessing.JoinableQueue()
        procs = []
        for _ in range(1, 5):
            proc = multiprocessing.Process(target=custom_pool_worker_wrapper,
                                           args=(args1, args2, results))
            proc.start()
            args1.put(fixed_data)
            procs.append(proc)
        args1.close()

        tmp = 0
        data = [1] * 100
        for i in range(1, iterations):
            tmp = 0
            for _ in range(1, 101):
                args2.put(data)
            for _ in range(1, 101):
                tmp += results.get()
                results.task_done()
        args2.close()
        args2.join()
        results.close()
        results.join()
        for proc in procs:
            proc.terminate()
        end_time = time.time()
        secs_per_iteration = (end_time - start_time) / iterations
        print("fixed_data {0:>13,} ints : {1:>6.6f} secs per iteration {2}"
              .format(len(fixed_data), secs_per_iteration, tmp))


fixed_data = None


def initializer(init_data):
    global fixed_data
    fixed_data = init_data


def builtin_pool_worker_wrapper(varying_data):
    return worker(varying_data, fixed_data)


def builtin_pool():
    iterations = 11
    for i in range(50, 83, 8):
        start_time = time.time()
        fixed_data = [i] * int(pow(10, i/10))
        pool = multiprocessing.Pool(4, initializer, (fixed_data,))
        data = [[1] * 100] * 100
        tmp = 0
        for i in range(1, iterations):
            tmp = sum(pool.map(builtin_pool_worker_wrapper, data))
        pool.close()
        pool.join()
        pool.terminate()
        end_time = time.time()
        secs_per_iteration = (end_time - start_time) / iterations
        print("fixed_data {0:>13,} ints : {1:>6.6f} seconds per iteration {2}"
              .format(len(fixed_data), secs_per_iteration, tmp))


class Pusher(object):

    def __init__(self):

        NUMBER_OF_PROCESSES = 5

        processes = list()

        q = multiprocessing.Queue() 

        for i in range(0, NUMBER_OF_PROCESSES):
            p=Processor(queue=q, idx=i)
            p.start()
            processes.append(p)

        start_time = time.time()
        do_ = True
        while do_:
            if q.empty():
                time.sleep(.003)
            else:
                print("RESULT: {0}".format(q.get()))

            if time.time() - start_time > 15:
                do_ = False
                break

        # wait till all complete
        [proc.join() for proc in processes]


if __name__ == "__main__":

    Pusher()

    print('. done.')




