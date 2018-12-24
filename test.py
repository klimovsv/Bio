import argparse
import time
from multiprocessing import Manager, Process

from misc.Algorithms import *
from misc.Reader import Reader


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('seq1', type=str)
    parser.add_argument('seq2', type=str)
    parser.add_argument('-g', '--gap', type=int, default=-2)
    parser.add_argument('-m', '--mapper', type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse()
    reader = Reader(arguments)
    gap = arguments.gap
    bigrams = reader.bigrams(reader.first_seq)

    alignments = align_sequences(reader.first_seq, reader.second_seq, reader.mapper, gap, bigrams)
    for result in alignments:
        score = result[0]
        align = result[1]
        if score > 0:
            with open('output_test.txt', 'w') as output_file:
                print('%d' % score, file=output_file)
                print(align, file=output_file)




