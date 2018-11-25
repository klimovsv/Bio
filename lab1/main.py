from misc.reader import Reader
import argparse


if __name__ == "__main__":
    reader = Reader({"first": "../fastafiles/first.fasta", "second": "../fastafiles/second.fasta", "mapper": ''})
    first, second = reader.first_seq, reader.seqond_seq
    first.print()
    second.print()
