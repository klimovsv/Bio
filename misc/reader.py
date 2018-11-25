class Reader:
    def __init__(self,config):
        self.first_seq = config['first']
        self.seqond_seq = config['second']
        self.mapper = config['mapper']
        self.NUCLEOTID_ALPH = set('A   T   G   C   S   W   R   Y   K   M   B   V   H   D   N'.split())
        self.AMINO_ALPH = set('A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  *'.split())

    def print(self):
        print(self.AMINO_ALPH)
        print(self.NUCLEOTID_ALPH)
        print(self.AMINO_ALPH - self.NUCLEOTID_ALPH)
        print(self.NUCLEOTID_ALPH - self.AMINO_ALPH)
