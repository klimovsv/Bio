from typing import Tuple, List

from misc.Mapper import Mapper

PairType = Tuple[int, int]


class Node:
    def __init__(self, start: PairType, end: PairType, score: int, k: int, diag_index: int):
        self.k = k
        self.start = start
        self.end = end
        self.next = []
        self.score = score
        self.diag_index = diag_index

    def add_edge(self, edge):
        self.next.append(edge)

    @property
    def node_len(self):
        return self.end[0] - self.start[0] + self.k - 2

    def __repr__(self):
        return "Start: %s. End: %s. Score: %s" % (self.start, self.end, self.score)


class Edge:
    def __init__(self, start, end, prec, succ, score):
        self.score = score
        self.start = start
        self.end = end
        self.prec = prec
        self.succ = succ


class Diag:
    def __init__(self, index: int):
        self.score = 0
        self.nodes = []
        self.index = index
        self.diag_start = self.calc_index

    def add(self, node):
        self.nodes.append(node)

    @property
    def calc_index(self):
        if self.index >= 0:
            return 0, self.index
        return abs(self.index), 0

    def diag_score(self, mapper: Mapper):
        self.score = 0
        for i in range(len(self.nodes) - 1):
            first_node = self.nodes[i]
            second_node = self.nodes[i + 1]
            start_ind = first_node.end
            end_ind = second_node.start
            cur_ind = (start_ind[0] + 1, start_ind[1] + 1)
            for _ in range(end_ind[0] - start_ind[0] - 1):
                score = mapper(cur_ind[0], cur_ind[1])
                self.score += score
                cur_ind = (cur_ind[0] + 1, cur_ind[1] + 1)

        self.score += sum(map(lambda node: node.score, self.nodes))
        return self.score

    @property
    def diag_len(self) -> int:
        return sum(node.node_len for node in self.nodes)

    def __repr__(self):
        return "{Nodes: %s. Diag index: %s. Score: %s}" % (self.nodes, self.diag_start, self.score)