import argparse
import time
from multiprocessing import Process,Manager

from misc.Algorithms import *
from misc.Reader import Reader
import operator

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gap', type=int, default=-2)
    parser.add_argument('seq1', type=str)
    parser.add_argument('-m', '--mapper', type=str, required=True)
    parser.add_argument('-d', '--database', type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse()
    reader = Reader(arguments)
    gap = arguments.gap
    bigrams = reader.bigrams(reader.first_seq)
    proc_num = 8
    procs = [None] * proc_num
    results = []


    # функция для выравнивания
    def perform_align(db, proc_number, lst):
        print("proc ", proc_number)
        start = time.time()
        res = []
        for item in db:
            alignments = align_sequences(reader.first_seq, item[1], reader.mapper, gap, bigrams)
            for result in alignments:
                score = result[0]
                align = result[1]
                if score > 0:
                    res.append((item[0], score, align))
        lst.append(res)
        elapsed_time = time.time() - start
        print("Process: %s, Time elasped: %s." % (proc_number, elapsed_time))


    # создание и запуск процессов
    start = time.time()
    manager = Manager()
    l = manager.list([])
    part_proc = len(reader.database) // proc_num

    for i in range(proc_num):
        procs[i] = Process(target=perform_align, args=(reader.database[part_proc * i:part_proc * (i + 1)], i, l))
        procs[i].start()

    for i in range(proc_num):
        procs[i].join()

    for res in l:
        results += res

    # сортировка по скору и запись в файлы output и results рабочей директории
    print('Number of seqs : {}'.format(len(results)))
    results.sort(key=operator.itemgetter(1), reverse=True)
    short_list = results[:]
    elapsed_time = time.time() - start
    print("Total time elapsed: %s" % elapsed_time)
    with open('output.txt', 'w') as f:
        with open('results.txt', 'w') as res:
            for ind, item in enumerate(short_list):
                print('%d. %s: %d' % (ind + 1, item[0], item[1]), file=f)
                print(item[2], file=f)
                print('{} {} {}'.format(ind + 1, item[0], item[1]), file=res)
