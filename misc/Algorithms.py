from misc.Seq import Seq


def lab1(mapper, reader, gap):
    first, second = reader.seqs

    F = [[gap * i for i in range(second.len()+1)]]
    for i in range(1,first.len()+1):
        F.append([i * gap])

    for i in range(1, first.len()+1):
        for j in range(1, second.len()+1):
            match = F[i - 1][j - 1] + mapper(i-1, j-1)
            delete = F[i - 1][j] + gap
            insert = F[i][j - 1] + gap
            maximum = max(match, delete, insert)
            F[i].append(maximum)

    print(len(F), len(F[0]))
    for i in range(len(F)):
        print(F[i])

    A = ""
    B = ""
    i = first.len()
    j = second.len()
    while i > 0 and j > 0:
        score = F[i][j]
        diag = F[i - 1][j - 1]
        up = F[i][j - 1]
        left = F[i - 1][j]
        if score == diag + mapper(i-1, j-1):
            A = first[i-1] + A
            B = second[j-1] + B
            i -= 1
            j -= 1
        elif score == up + gap:
            A = "-" + A
            B = second[j-1] + B
            j -= 1
        elif score == left + gap:
            A = first[i-1] + A
            B = "-" + B
            i -= 1

    while i > 0:
        A = first[i-1] + A
        B = "-" + B
        i -= 1

    while j > 0:
        A = '-' + A
        B = second[j-1] + B
        j -= 1

    return A, B, F[first.len()][second.len()], first, second
