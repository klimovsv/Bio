from misc.Reader import Reader
from misc.Mapper import Mapper
from misc.Algorithms import *
import argparse


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
    first, second = reader.seqs
    # print(reader.seqs)
    mapper = Mapper(reader.mapper, first, second)
    gap = arguments.gap
    # firstal, secondal, score, first, second = lab1(mapper, reader, gap)
    # print(firstal)
    # print(secondal)
    # print(score)
    # lab1(mapper, reader, gap)
    # lab2(mapper, reader, gap)
    # smith_waterman(first, second, gap, reader.mapper)
    align_sequences(first[1:], second[1:], reader.mapper, gap)
    smith_waterman(first, second, gap, reader.mapper, -100, 100)
