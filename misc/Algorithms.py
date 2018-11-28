def empty_table(n, m):
    table = []
    for i in range(n):
        table.append([None for _ in range(m)])
    return table


def lab1(mapper, reader, gap):
    first, second = reader.seqs

    firstlen = len(first)
    secondlen = len(second)

    F = empty_table(firstlen + 1, secondlen + 1)

    for i in range(firstlen + 1):
        F[i][0] = gap * i
    for i in range(secondlen + 1):
        F[0][i] = gap * i

    # F = [[gap * i for i in range(second.len()+1)]]
    # for i in range(1,first.len()+1):
    #     F.append([i * gap])

    for i in range(1, firstlen + 1):
        for j in range(1, secondlen + 1):
            match = F[i - 1][j - 1] + mapper(i - 1, j - 1)
            delete = F[i - 1][j] + gap
            insert = F[i][j - 1] + gap
            maximum = max(match, delete, insert)
            F[i][j]= maximum

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
        up = F[i][j - 1]
        left = F[i - 1][j]
        if score == diag + mapper(i - 1, j - 1):
            A = first[i - 1] + A
            B = second[j - 1] + B
            i -= 1
            j -= 1
        elif score == up + gap:
            A = "-" + A
            B = second[j - 1] + B
            j -= 1
        elif score == left + gap:
            A = first[i - 1] + A
            B = "-" + B
            i -= 1

    while i > 0:
        A = first[i - 1] + A
        B = "-" + B
        i -= 1

    while j > 0:
        A = '-' + A
        B = second[j - 1] + B
        j -= 1

    return A, B, F[firstlen][secondlen], first, second
