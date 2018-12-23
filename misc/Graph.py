from typing import Tuple

from misc.Mapper import Mapper

PairType = Tuple[int, int]


class Node:
    def __init__(self, start: PairType, end: PairType, score: int, k: int, diag_index: int):
        self.k = k
        self.checked = False
        self.component_nmb = None
        self.start = start
        self.end = end
        self.next = []
        self.prev = []
        self.score = score
        self.root = False
        self.diag_index = diag_index

    def add_next(self, edge):
        self.next.append(edge)

    def add_prev(self, edge):
        self.prev.append(edge)

    def is_reachable(self, node):
        start = self.start
        end = node.start
        return end[0] >= start[0] and end[1] >= start[1] and (end[0] != start[0] or end[1] != start[1])

    def get_dist(self, node):
        start = self.end
        end = node.start
        if end[0] >= start[0] and end[1] >= start[1]:
            return end[0] - start[0], end[1] - start[1]
        elif end[1] > end[0] + self.diag_index:
            return 0, abs(end[0] - (end[1] - self.diag_index))
        else:
            return abs(end[0] - (end[1] - self.diag_index)), 0

    @property
    def node_len(self):
        return self.end[0] - self.start[0] + self.k - 2

    def __repr__(self):
        return "Start: %s. End: %s. Score: %s uid : %s" % (self.start, self.end, self.score, self.uid)

    def __eq__(self, node):
        return node.start == self.start and node.end == self.end


class Edge:
    def __init__(self, prev_node, next_node, score):
        self.prev = prev_node
        self.next = next_node
        self.score = score


class Diag:
    def __init__(self, index: int):
        self.score = 0
        self.nodes = []
        self.index = index
        self.dots = []
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
        start, end = self.dots[0], (self.dots[-1][0] + 2, self.dots[-1][1] + 2)
        tmp = start
        while tmp != end:
            self.score += mapper(tmp[0], tmp[1])
            tmp = (tmp[0] + 1, tmp[1] + 1)
        return self.score

    @property
    def diag_len(self) -> int:
        return len(self.dots)
        # return sum(node.node_len for node in self.nodes)

    def __repr__(self):
        return "{Nodes: %s. Diag index: %s. Score: %s}" % (self.nodes, self.diag_start, self.score)
