from misc.Graph import *
from misc.Mapper import Mapper
from typing import List, Dict
import operator

TableType = Dict[str, Dict[str, int]]


def empty_table(n, m):
    table = []
    for i in range(n):
        table.append([0 for _ in range(m)])
    return table


def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])
    print()


def smith_waterman(seq1, seq2, gap, table, b_min: int, b_max: int, a_min: int, a_max: int):
    len1 = len(seq1)
    len2 = len(seq2)

    INS = 1
    DEL = 2
    STOP = 3
    DIAG = 0

    start = max(0,(a_min-b_max)//2)
    end = min(len1 - 1,(a_max-b_min)//2)
    # ranges between y = x + b_min and y = x + b_max
    #                y = -x + a_min and y = -x + a_max

    def limit(_i, _j):
        return len1 > _i >= 0 and len2 > _j >= 0

    def in_range(_i: int, _j: int) -> bool:
        return _i + b_max >= _j >= _i + b_min and _i + a_max >= _j >= _i + a_min and limit(_i, _j)

    def get_intersection(_i: int):
        return max(0, _i + a_min, _i + b_min), min(len2 - 1, _i + a_max, _i + b_max)

    def set_element(d: dict, el, i: int, j: int):
        if d.get(i) is None:
            d[i] = {}
        d[i][j] = el

    mapper = Mapper(table, seq1, seq2)
    max_element = ((-1, -1), (-1, -1))
    # F = empty_table(len1 + 1, len2 + 1)

    M = {}

    # for i in range(len1 + 1):
    #     F[i][0] = (0, STOP)
    #
    # for i in range(len2 + 1):
    #     F[0][i] = (0, STOP)

    for i in range(start, end + 1):
        ranges = get_intersection(i)
        for j in range(ranges[0], ranges[1] + 1):
            maximums = [(0, STOP)]
            if in_range(i - 1, j - 1):
                match = M[i - 1][j - 1][0] + mapper(i, j)
                maximums.append((match, DIAG))

            if in_range(i - 1, j):
                insert = M[i - 1][j][0] + gap
                maximums.append((insert, INS))

            if in_range(i, j - 1):
                delete = M[i][j - 1][0] + gap
                maximums.append((delete, DEL))

            maximum = max(maximums)
            if maximum[0] >= max_element[0][0]:
                max_element = (maximum, (i, j))
            # M[i][j] = maximum
            set_element(M, maximum, i, j)

    # for i in range(1, len1 + 1):
    #     # ranges = get_intersection(i)
    #     for j in range(1, len2 + 1):
    #         maximums = [(0, STOP)]
    #         if in_range(i - 1, j - 1):
    #             match = F[i - 1][j - 1][0] + mapper(i, j)
    #             maximums.append((match, DIAG))
    #
    #         if in_range(i - 1, j):
    #             insert = F[i - 1][j][0] + gap
    #             maximums.append((insert, INS))
    #
    #         if in_range(i, j - 1):
    #             delete = F[i][j - 1][0] + gap
    #             maximums.append((delete, DEL))
    #
    #         maximum = max(maximums)
    #         if maximum[0] >= max_element[0][0]:
    #             max_element = (maximum, (i, j))
    #         F[i][j] = maximum
    #         # M[i][j] = maximum
    #         set_element(M, maximum, i, j)

    # print(M)

    i = max_element[1][0]
    j = max_element[1][1]
    A = ""
    B = ""
    while M[i][j][1] != STOP:
        if M[i][j][1] == DIAG:
            A = seq1[i] + A
            B = seq2[j] + B
            i -= 1
            j -= 1
        elif M[i][j][1] == INS:
            A = seq1[i] + A
            B = "-" + B
            i -= 1
        elif M[i][j][1] == DEL:
            A = "-" + A
            B = seq2[j] + B
            j -= 1

    # print("Score : {}".format(max_element[0][0]))
    return max_element[0][0] , fine_print((A, B), (i + 1, max_element[1][0]), (j + 1, max_element[1][1]), (seq1, seq2))


def fine_print(*args):
    A, B = args[0]
    iA, jA = args[1]
    iB, jB = args[2]
    seq1, seq2 = args[3]
    res = ''
    if iA > iB:
        res+=(seq1[:iA] + A + seq1[jA + 1:]) + '\n'
        res+=(" " * iA + "|" * len(A))+ '\n'
        res+=(" " * (iA - iB) + seq2[:iB] + B + seq2[jB + 1:])+ '\n'
    elif iA < iB:
        res+=(" " * (iB - iA) + seq1[:iA] + A + seq1[jA + 1:])+ '\n'
        res+=(" " * (iB ) + "|" * len(A))+ '\n'
        res+=(seq2[:iB] + B + seq2[jB + 1:])+ '\n'
    elif iA == iB:
        res+=(seq1[:iA] + A + seq1[jA + 1:])+ '\n'
        res+=(" " * (iB) + "|" * len(A))+ '\n'
        res+=(seq2[:iB] + B + seq2[jB + 1:])+ '\n'
    return res


def create_diags_with_nodes(seq1: str, seq2: str, table: TableType) -> List[Diag]:
    mapper = Mapper(table, seq1, seq2)
    len1 = len(seq1)
    len2 = len(seq2)
    k_gram = 2
    M = empty_table(len1, len2)

    def limit(_i, _j):
        return _i < len1 and _j < len2

    diags = []
    for i in range(-len1 + 1, len2):
        diags.append(Diag(i))

    for diag in diags:
        i, j = diag.diag_start
        while limit(i, j):
            start_node = (i, j)
            score = 0
            node_len = 0
            while limit(i, j) and seq1[i] == seq2[j]:
                # M[i][j] = mapper(i, j)
                score += mapper(i, j)
                i += 1
                j += 1
                node_len += 1

            end_node = (i, j)
            if end_node != start_node and node_len >= k_gram:
                end_node = (i - 1, j - 1)
                diag.add(Node(start_node, end_node, score, k_gram, diag.index))
            i += 1
            j += 1

    return diags

    # N = empty_table(len1, len2)
    # print_matrix(N)
    # for diag in diags:
    #     for node in diag.nodes:
    #         i, j = node.start
    #         ie, je = node.end
    #         while i <= ie and j <= je:
    #             N[i][j] = 1111
    #             i += 1
    #             j += 1

    # [diag.diag_score() for diag in diags]
    # diags = list(filter(lambda d: d.score != 0, diags))
    # [print(diag.score) for diag in diags]
    # sorted_diags = sorted(diags, key=lambda d: d.score)[len(diags) // 2:]
    # print()
    # [print(diag.score) for diag in sorted_diags]
    #
    # print_matrix(N)
    # print_matrix(M)


def gen_new_path(path, next_node, score):
    max_diag_ind = path[1]
    min_diag_ind = path[0]
    new_max = max_diag_ind
    new_min = min_diag_ind
    new_score = score
    if next_node.diag_index > max_diag_ind:
        new_max = next_node.diag_index
    if next_node.diag_index < min_diag_ind:
        new_min = next_node.diag_index
    return new_min, new_max, new_score, path[3], next_node


def traverse(node: Node, path: Tuple):
    edges = node.next
    paths = []
    score = path[2]
    for edge in edges:
        next_node = edge.next
        p = gen_new_path(path, next_node, score + edge.score + next_node.score)
        paths += traverse(next_node, p)

    if len(edges) == 0:
        return [path]
    else:
        return paths


def align_sequences(seq1: str, seq2: str, table: TableType, gap: int):
    diags = create_diags_with_nodes(seq1, seq2, table)
    mapper = Mapper(table, seq1, seq2)

    min_diag_len = 1
    max_diag_num = 10
    min_diag_score = 10

    diags = [diag for diag in diags if diag.diag_len >= min_diag_len]
    diags = [diag for diag in diags if diag.diag_score(mapper) > min_diag_score]
    if not diags:
        return -1, ''

    diags.sort(key=operator.attrgetter("score"), reverse=True)

    diags = diags[:max_diag_num]

    nodes = []
    for diag in diags:
        nodes += diag.nodes

    # сортировка веришн
    # nodes.sort(key=operator.attrgetter("start"))
    # print(nodes)

    # построение графа
    for i in range(len(nodes)):
        node = nodes[i]
        for j in range(i + 1, len(nodes)):
            next_node = nodes[j]
            if node.is_reachable(next_node):
                gap_score = node.get_dist(next_node) * gap
                # print(gap_score)
                sum_wtih_gap = node.score + next_node.score + gap_score
                if node.score <= sum_wtih_gap:
                    edge = Edge(node, next_node, gap_score)
                    node.add_next(edge)
                    next_node.add_prev(edge)

    # определение стартовых вершин и обход в глубину
    paths = []
    for node in nodes:
        # print(node.diag_index)
        if len(node.prev) == 0:
            paths += traverse(node, (node.diag_index, node.diag_index, node.score, node, node))
    optimal_path = sorted(paths, key=lambda path: path[2])[-1]

    # print(paths)
    b_min = optimal_path[0] - 32
    b_max = optimal_path[1] + 32
    a_min = sum(optimal_path[3].start) - 32
    a_max = sum(optimal_path[4].end) + 32
    res_score , res_alignment = smith_waterman(seq1, seq2, gap, table, b_min, b_max, a_min, a_max)
    # print(optimal_path)
    # print(b_min, b_max, a_min, a_max)

    # N = empty_table(len(seq1), len(seq2))
    # for diag in diags:
    #     for node in diag.nodes:
    #         i, j = node.start
    #         ie, je = node.end
    #         while i <= ie and j <= je:
    #             N[i][j] = 1
    #             i += 1
    #             j += 1
    # print_matrix(N)
    return res_score, res_alignment

