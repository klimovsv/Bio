class Seq:
    def __init__(self, seq):
        self.seq = seq

    def len(self):
        return len(self.seq)

    def __str__(self):
        return self.seq

    def __getitem__(self, item):
        return self.seq[item]
