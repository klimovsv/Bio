from misc.Seq import Seq
import json


class Reader:
    def __init__(self, config):
        self.config = config
        self.first_seq = self.read_seq(config.seq1)
        self.seqond_seq = self.read_seq(config.seq2)
        self.mapper = self.load_mapper(config.mapper)
        self.NUCLEOTID_ALPH = set('A   T   G   C   S   W   R   Y   K   M   B   V   H   D   N'.split())
        self.AMINO_ALPH = set('A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  *'.split())

    def read_seq(self, file_name):
        with open(file_name, 'r') as file:
            return Seq(file.read())

    def print(self):
        print(self.AMINO_ALPH)
        print(self.NUCLEOTID_ALPH)
        print(self.AMINO_ALPH - self.NUCLEOTID_ALPH)
        print(self.NUCLEOTID_ALPH - self.AMINO_ALPH)

    def load_mapper(self, mapper):
        with open(mapper, 'r') as f:
            return json.load(f)
