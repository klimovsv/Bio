class Mapper:
    def __init__(self, mapper, seq1, seq2):
        self.mapper = mapper
        self.seq1 = seq1
        self.seq2 = seq2

    def __call__(self, *args, **kwargs):
        if len(args) != 2:
            raise Exception('need 2 arguments')
        else:
            i = args[0]
            j = args[1]
            return self.mapper[self.seq1[i]][self.seq2[j]]
