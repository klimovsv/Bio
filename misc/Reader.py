import json


class Reader:
    def __init__(self, config):
        self.config = config
        self.mapper = self.load_mapper(config.mapper)
        self.first_seq = self.read_seq(config.seq1)
        self.out = config.o
        self.seqond_seq = self.read_seq(config.seq2)
        self.seqs = (" " + self.first_seq, " " + self.seqond_seq)

    def read_seq(self, file_name):
        with open(file_name, 'r') as file:
            lines = list(filter(lambda x: len(x.strip()) != 0, file.read().splitlines()[1:]))
            # print(lines)
            if len(lines) == 0:
                raise Exception("empty sequence")
            for line in lines:
                for c in line:
                    if c not in self.mapper.keys():
                        raise Exception(
                            "invalid character \"{}\" for mapper {} in seq : {}".format(c, self.config.mapper,
                                                                                        file_name))
            return ''.join(lines)

    def load_mapper(self, mapper):
        with open(mapper, 'r') as f:
            return json.load(f)

    def output(self, seq1, seq2, score):
        s1 = []
        s2 = []
        while len(seq1)//100 != 0:
            s1.append(seq1[:100])
            s2.append(seq2[:100])
            seq1 = seq1[100:]
            seq2 = seq2[100:]

        s1.append(seq1)
        s2.append(seq2)

        with open(self.out,"w+")as f:
            f.write("Score : {}\n".format(score))
            for i in range(len(s1)):
                f.write("{}\n".format(s1[i]))
                f.write("{}\n".format(s2[i]))


        if self.out:
            print(self.out)

    def fine_print(self,*args):
        A , B = args[0]
        iA , jA = args[1]
        iB , jB = args[2]
        seq1 , seq2 = args[3]

