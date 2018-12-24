import argparse
import time
from multiprocessing import Manager, Process

from misc.Algorithms import *
from misc.Reader import Reader


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gap', type=int, default=-2)
    parser.add_argument('seq1', type=str)
    parser.add_argument('-m', '--mapper', type=str, required=True)
    parser.add_argument('-d', '--database', type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    start = time.time()
    arguments = parse()
    reader = Reader(arguments)
    gap = arguments.gap
    bigrams = reader.bigrams(reader.first_seq)
    proc_num = 8

    # функция для выравнивания
    def perform_align(db, proc_number, lst):
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
        print("Process: %s, Time elapsed: %.2f" % (proc_number, elapsed_time))


    # создание и запуск процессов
    manager = Manager()
    l = manager.list([])
    part_proc = len(reader.database) // proc_num

    procs = [Process(target=perform_align, args=(reader.database[part_proc * i:part_proc * (i + 1)], i, l))
             for i in range(proc_num)]
    for proc in procs:
        proc.start()

    for i in range(proc_num):
        procs[i].join()

    results = []
    for res_file in l:
        results += res_file

    # сортировка по скору и запись в файлы output и results рабочей директории
    print('Number of seqs : {}'.format(len(results)))
    results.sort(key=operator.itemgetter(1), reverse=True)
    short_list = results[:]
    with open('output.txt', 'w') as output_file:
        with open('results.txt', 'w') as res_file:
            for ind, item in enumerate(short_list):
                print('%d %s %d' % (ind + 1, item[0], item[1]), file=output_file)
                print(item[2], file=output_file)
                print('{} {} {}'.format(ind + 1, item[0], item[1]), file=res_file)
    elapsed_time = time.time() - start
    print("Total time elapsed: %.2f" % elapsed_time)
