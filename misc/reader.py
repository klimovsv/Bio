from misc.Seq import Seq


class Reader:
    def __init__(self, config):
        self.config = config
        self.first_seq = self.read_seq(config['first'])
        self.seqond_seq = self.read_seq(config['second'])
        self.mapper = config['mapper']
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
