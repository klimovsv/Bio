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
    seq1, seq2, table, bigrams_ind = reader.first_seq, reader.second_seq, reader.mapper, bigrams
    diags = create_diags_with_nodes(seq1, seq2, table, bigrams_ind)
    assert repr(diags) == "[{Nodes: [Start: (0, 10). End: (5, 15). Score: 31, Start: (7, 17). End: (15, 25). Score: 71]. " \
                          "Diag index: (0, 10). Score: 100}]"
    alignments = align_sequences(seq1, seq2, table, gap, bigrams_ind)
    for result in alignments:
        score = result[0]
        align = result[1]
        if score > 0:
            with open('output_test.txt', 'w') as output_file:
                print('%d' % score, file=output_file)
                print(align, file=output_file)
