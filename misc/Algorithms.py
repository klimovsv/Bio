def empty_table(n, m):
    table = []
    for i in range(n):
        table.append([None for _ in range(m)])
    return table


def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])
    print()


def lab1(mapper, reader, gap):
    first, second = reader.seqs

    firstlen = len(first) - 1
    secondlen = len(second) - 1

    F = empty_table(firstlen + 1, secondlen + 1)

    for i in range(firstlen + 1):
        F[i][0] = gap * i
    for i in range(secondlen + 1):
        F[0][i] = gap * i

    for i in range(1, firstlen + 1):
        for j in range(1, secondlen + 1):
            match = F[i - 1][j - 1] + mapper(i, j)
            insert = F[i - 1][j] + gap
            delete = F[i][j - 1] + gap
            maximum = max(match, delete, insert)
            F[i][j] = maximum

    print(len(F), len(F[0]))
    for i in range(len(F)):
        print(F[i])

    A = ""
    B = ""
    i = firstlen
    j = secondlen
    while i > 0 and j > 0:
        score = F[i][j]
        diag = F[i - 1][j - 1]
        up = F[i - 1][j]
        left = F[i][j - 1]
        if score == diag + mapper(i, j):
            A = first[i] + A
            B = second[j] + B
            i -= 1
            j -= 1
        elif score == left + gap:
            A = "-" + A
            B = second[j] + B
            j -= 1
        elif score == up + gap:
            A = first[i] + A
            B = "-" + B
            i -= 1

    while i > 0:
        A = first[i] + A
        B = "-" + B
        i -= 1

    while j > 0:
        A = '-' + A
        B = second[j] + B
        j -= 1

    print(A)
    print(B)
    print(F[firstlen][secondlen])
    return A, B, F[firstlen][secondlen], first, second


def lab2(mapper, reader, opengap, extended=-1):
    first, second = reader.seqs

    firstlen = len(first) - 1
    secondlen = len(second) - 1

    M = empty_table(firstlen + 1, secondlen + 1)
    In = empty_table(firstlen + 1, secondlen + 1)
    D = empty_table(firstlen + 1, secondlen + 1)
    R = empty_table(firstlen + 1, secondlen + 1)

    infinity = 2 * opengap + (firstlen + secondlen + 2) * extended + 1
    for i in range(len(M)):
        M[i][0] = infinity
        D[i][0] = infinity
        In[i][0] = opengap + (i - 1) * extended

    for i in range(len(M[0])):
        M[0][i] = infinity
        In[0][i] = infinity
        D[0][i] = opengap + (i - 1) * extended

    M[0][0] = 0
    D[0][0] = In[0][0] = infinity

    for i in range(1, firstlen + 1):
        for j in range(1, secondlen + 1):
            M[i][j] = max(M[i - 1][j - 1] + mapper(i, j), In[i - 1][j - 1] + mapper(i, j),
                          D[i - 1][j - 1] + mapper(i, j))
            D[i][j] = max(D[i][j - 1] + extended, M[i][j - 1] + opengap, In[i][j - 1] + opengap)
            In[i][j] = max(In[i - 1][j] + extended, M[i - 1][j] + opengap, In[i - 1][j] + opengap)

    for i in range(firstlen + 1):
        for j in range(secondlen + 1):
            R[i][j] = max((D[i][j], 1), (In[i][j], 2), (M[i][j], 0))

    A = ""
    B = ""
    i = firstlen
    j = secondlen
    while i > 0 and j > 0:
        direction = R[i][j][1]
        if direction == 0:
            A = first[i] + A
            B = second[j] + B
            i -= 1
            j -= 1
        elif direction == 1:
            A = "-" + A
            B = second[j] + B
            j -= 1
        elif direction == 2:
            A = first[i] + A
            B = "-" + B
            i -= 1

    while i > 0:
        A = first[i] + A
        B = "-" + B
        i -= 1

    while j > 0:
        A = '-' + A
        B = second[j] + B
        j -= 1

    print(A)
    print(B)
    print(R[firstlen][secondlen][0])
    reader.output(A, B, R[firstlen][secondlen][0])


def smith_waterman(seq1, seq2, gap, table):
    from misc.Mapper import Mapper
    len1 = len(seq1) - 1
    len2 = len(seq2) - 1

    INS = 1
    DEL = 2
    STOP = 3
    DIAG = 0

    mapper = Mapper(table, seq1, seq2)
    max_element = ((-1, -1), (-1, -1))
    F = empty_table(len1 + 1, len2 + 1)

    for i in range(len1 + 1):
        F[i][0] = (0, STOP)

    for i in range(len2 + 1):
        F[0][i] = (0, STOP)

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            match = F[i - 1][j - 1][0] + mapper(i, j)
            insert = F[i - 1][j][0] + gap
            delete = F[i][j - 1][0] + gap
            maximum = max((match, DIAG), (delete, DEL), (insert, INS), (0, STOP))
            if maximum[0] >= max_element[0][0]:
                max_element = (maximum, (i, j))
            F[i][j] = maximum

    print_matrix(F)

    i = max_element[1][0]
    j = max_element[1][1]
    A = ""
    B = ""
    while F[i][j][1] != STOP:
        if F[i][j][1] == DIAG:
            A = seq1[i] + A
            B = seq2[j] + B
            i -= 1
            j -= 1
        elif F[i][j][1] == INS:
            A = seq1[i] + A
            B = "-" + B
            i -= 1
        elif F[i][j][1] == DEL:
            A = "-" + A
            B = seq2[j] + B
            j -= 1

    print("Score : {}".format(max_element[0][0]))
    fine_print((A, B), (i + 1, max_element[1][0]), (j + 1, max_element[1][1]), (seq1, seq2))


def fine_print(*args):
    A, B = args[0]
    iA, jA = args[1]
    iB, jB = args[2]
    seq1, seq2 = args[3]
    if iA > iB:
        print(seq1[1:iA] + A + seq1[jA + 1:])
        print(" " * (iA-1) + "|" * len(A))
        print(" " * (iA - iB - 1) + seq2[:iB] + B + seq2[jB + 1:])
    elif iA < iB:
        print(" " * (iB - iA - 1) + seq1[:iA] + A + seq1[jA + 1:])
        print(" " * (iB - 1) + "|" * len(A))
        print(seq2[1:iB] + B + seq2[jB + 1:])
    elif iA == iB:
        print(seq1[1:iA] + A + seq1[jA + 1:])
        print(" " * (iB - 1) + "|" * len(A))
        print(seq2[1:iB] + B + seq2[jB + 1:])
