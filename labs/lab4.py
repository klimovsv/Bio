from misc.Reader import Reader
from misc.Mapper import Mapper
from misc.Algorithms import *
import argparse
import time
from multiprocessing import Lock, Process, Array, Value, Queue

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gap', type=int, default=-2)
    parser.add_argument('seq1', type=str)
    parser.add_argument('seq2', type=str)
    parser.add_argument('-o', type=str, required=False)
    parser.add_argument('-m', '--mapper', type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse()
    reader = Reader(arguments)
    reader.read_database('/home/sergey/Downloads/base.json')
    first, second = reader.seqs
    # print(reader.seqs)
    mapper = Mapper(reader.mapper, first, second)
    gap = arguments.gap
    bigrams = reader.bigrams(reader.first_seq)
    # firstal, secondal, score, first, second = labs(mapper, reader, gap)
    # print(firstal)
    # print(secondal)
    # print(score)
    # labs(mapper, reader, gap)
    # lab2(mapper, reader, gap)
    # smith_waterman(first, second, gap, reader.mapper)
    # align_sequences(first[1:], second[1:], reader.mapper, gap)
    # smith_waterman(first[1:], second[1:], gap, reader.mapper, -100, 100,-100,100)
    n = 8
    procs = [None] * n
    results = []


    def perform_align(db, i, q):
        res = []
        start = time.time()
        for item in db:
            score, align = align_sequences(reader.first_seq, item[1], reader.mapper, gap, bigrams)
            if score > 0:
                res += [(item[0], score, align)]
        q.put(res)
        print(i, time.time() - start)



    start = time.time()
    q = Queue()

    part = len(reader.database) // n
    part_proc = len(reader.database) // n

    for i in range(len(procs)):
        procs[i] = Process(target=perform_align, args=(reader.database[part_proc * i:part_proc * (i + 1)], i, q))
        procs[i].start()

    for i in range(len(procs)):
        procs[i].join()

    while not q.empty():
        results += q.get()

    print(time.time() - start)
    results.sort(key=lambda x: x[1], reverse=True)
    short_list = results[:10]
    for ind, item in enumerate(short_list):
        print('%d. %s: %d' % (ind + 1, item[0], item[1]))
        print(item[2])
