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

    start = max((a_min - b_max) // 2, 0)
    end = min(len1 - 1, (a_max - b_min) // 2)

    def limit(_i, _j):
        return len1 > _i >= 0 and len2 > _j >= 0

    def in_range(_i: int, _j: int) -> bool:
        return _i + b_max >= _j >= _i + b_min and -_i + a_max >= _j >= -_i + a_min and limit(_i, _j)

    def get_intersection(_i: int):
        return max(0, -_i + a_min, _i + b_min), min(len2 - 1, - _i + a_max, _i + b_max)

    def set_element(d: dict, el, i: int, j: int):
        if d.get(i) is None:
            d[i] = {}
        d[i][j] = el

    mapper = Mapper(table, seq1, seq2)
    max_element = ((-1, -1), (-1, -1))

    M = {}

    for i in range(start, end + 1):
        ranges = get_intersection(i)
        for j in range(ranges[0], ranges[1] + 1):
            maximums = [(0, STOP)]

            if not in_range(i - 1, j - 1):
                set_element(M, (0, STOP), i - 1, j - 1)
            if not in_range(i - 1, j):
                set_element(M, (0, STOP), i - 1, j)
            if not in_range(i, j - 1):
                set_element(M, (0, STOP), i, j - 1)
            delete = (M[i][j - 1][0] + gap, DEL)
            insert = (M[i - 1][j][0] + gap, INS)
            match = (M[i - 1][j - 1][0] + mapper(i, j), DIAG)
            maximums += [delete, insert, match]

            maximum = max(maximums)
            if maximum[0] >= max_element[0][0]:
                max_element = (maximum, (i, j))
            set_element(M, maximum, i, j)

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

    return max_element[0][0], fine_print((A, B), (i + 1, max_element[1][0]), (j + 1, max_element[1][1]), (seq1, seq2))


def fine_print(*args):
    A, B = args[0]
    iA, jA = args[1]
    iB, jB = args[2]
    seq1, seq2 = args[3]
    res = ''
    if iA > iB:
        res += (seq1[:iA] + A + seq1[jA + 1:]) + '\n'
        res += (" " * iA + "|" * len(A)) + '\n'
        res += (" " * (iA - iB) + seq2[:iB] + B + seq2[jB + 1:]) + '\n'
    elif iA < iB:
        res += (" " * (iB - iA) + seq1[:iA] + A + seq1[jA + 1:]) + '\n'
        res += (" " * iB + "|" * len(A)) + '\n'
        res += (seq2[:iB] + B + seq2[jB + 1:]) + '\n'
    elif iA == iB:
        res += (seq1[:iA] + A + seq1[jA + 1:]) + '\n'
        res += (" " * iB + "|" * len(A)) + '\n'
        res += (seq2[:iB] + B + seq2[jB + 1:]) + '\n'
    return res


def create_diags_with_nodes(seq1: str, seq2: str, table: TableType, bigrams_ind: dict) -> List[Diag]:
    mapper = Mapper(table, seq1, seq2)
    len1 = len(seq1)
    len2 = len(seq2)
    k_gram = 2

    index_to_diag = {}

    for j in range(len2 - 1):
        bigram = seq2[j:j + 2]
        indexs_in_first_seq = bigrams_ind.get(bigram)
        if not indexs_in_first_seq is None:
            for i in indexs_in_first_seq:
                diag_index = j - i
                diag = index_to_diag.get(diag_index)
                if diag is None:
                    index_to_diag[diag_index] = Diag(diag_index)
                    diag = index_to_diag[diag_index]
                diag.dots += [(i, j)]

    min_diag_len = 100
    max_diag_num = 10
    min_diag_score = 300

    diags = index_to_diag.values()
    diags = [diag for diag in diags if diag.diag_len >= min_diag_len]
    diags = sorted(diags, key=operator.attrgetter("diag_len"), reverse=True)[:max_diag_num]
    diags = [diag for diag in diags if diag.diag_score(mapper) > min_diag_score]

    if not diags:
        return diags

    for diag in diags:
        i, j = diag.dots[0]
        i_end = diag.dots[-1][0] + 1
        j_end = diag.dots[-1][1] + 1
        while i <= i_end and j <= j_end:
            start_node = (i, j)
            score = 0
            node_len = 0
            while i <= i_end and j <= j_end and seq1[i] == seq2[j]:
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


def closure(n):
    def inner():
        return n

    return inner


def traverse(node: Node, path: Tuple, gap: int, depth: int):
    paths = []
    score = path[2]
    for edge in node.next:
        next_node = edge.next
        p = gen_new_path(path, next_node, score + edge.score + next_node.score)
        paths += traverse(next_node, p, gap, depth + 1)
        paths.sort(key=operator.itemgetter(2), reverse=True)
        paths = [paths[0]]

    if len(node.next) == 0:
        return [path]
    else:
        return paths


def align_sequences(seq1: str, seq2: str, table: TableType, gap: int, bigrams_ind: dict):
    diags = create_diags_with_nodes(seq1, seq2, table, bigrams_ind)

    if not diags:
        return [(-1, '')]

    nodes = []
    for diag in diags:
        nodes += diag.nodes

    # сортировка веришн
    nodes.sort(key=operator.attrgetter("start"))

    # построение графа
    for i in range(len(nodes)):
        node = nodes[i]
        for j in range(len(nodes)):
            next_node = nodes[j]
            if node.is_reachable(next_node):
                dist = node.get_dist(next_node)
                assert dist[0] > 0 and dist[1] > 0 or dist[0] == 0 and dist[1] > 0 or dist[0] > 0 and dist[1] == 0
                gap_score = (dist[0] + dist[1]) * gap
                assert gap_score < 0
                sum_wtih_gap = node.score + next_node.score + gap_score
                if node.score <= sum_wtih_gap:
                    edge = Edge(node, next_node, gap_score)
                    node.add_next(edge)
                    next_node.add_prev(edge)

    paths = []

    def visit(n : Node):
        n.checked = True
        for edg in n.next:
            next = edg.next
            if not next.checked:
                next.component_nmb = n.component_nmb
                visit(next)
        for edg in n.prev:
            next = edg.prev
            if not next.checked:
                next.component_nmb = n.component_nmb
                visit(next)

    comp_set = set()
    components_nmb = 0
    for node in nodes:
        if not node.checked:
            components_nmb += 1
            comp_set.add(components_nmb)
            node.component_nmb = components_nmb
            visit(node)

    # print(components_nmb)
    for node in nodes:
        if len(node.prev) == 0:
            paths += traverse(node, (node.diag_index, node.diag_index, node.score, node, node), gap, 0)

    paths.sort(key=lambda path: path[2], reverse=True)
    optimal_paths = []
    for path in paths:
        path_comp_nmb = path[4].component_nmb
        if path_comp_nmb in comp_set:
            optimal_paths.append(path)
            comp_set.remove(path_comp_nmb)

    results = []
    for path in optimal_paths:
        tmp = 32
        b_min = path[0] - tmp
        b_max = path[1] + tmp
        a_min = sum(path[3].start) - tmp
        a_max = sum(path[4].end) + tmp
        results += [smith_waterman(seq1, seq2, gap, table, b_min, b_max, a_min, a_max)]
    return results
