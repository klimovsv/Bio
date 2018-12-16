import json


class Reader:
    def __init__(self, config):
        self.config = config
        self.mapper = self.load_mapper(config.mapper)
        self.first_seq = self.read_seq(config.seq1)
        self.second_seq = self.read_seq(config.seq2)
        self.database = []
        self.out = config.o
        self.seqs = (" " + self.first_seq, " " + self.second_seq)

    def read_database(self,filename):
        with open(filename,'r') as f:
            self.database = json.load(f)
        # print(len(self.database))
        # print(len(self.database[0]))

    def bigrams(self, seq):
        bigrams = {}
        for i in range(len(seq)-1):
            if bigrams.get(seq[i:i+2]) is None:
                bigrams[seq[i:i+2]] = []
            bigrams[seq[i:i + 2]] += [i]
        return bigrams

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

    @staticmethod
    def load_mapper(mapper):
        with open(mapper, 'r') as f:
            return json.load(f)

    def output(self, seq1, seq2, score):
        s1 = []
        s2 = []
        while len(seq1) // 100 != 0:
            s1.append(seq1[:100])
            s2.append(seq2[:100])
            seq1 = seq1[100:]
            seq2 = seq2[100:]

        s1.append(seq1)
        s2.append(seq2)

        with open(self.out, "w+")as f:
            f.write("Score : {}\n".format(score))
            for i in range(len(s1)):
                f.write("{}\n".format(s1[i]))
                f.write("{}\n".format(s2[i]))

        if self.out:
            print(self.out)