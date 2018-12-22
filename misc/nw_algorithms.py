from misc.Algorithms import empty_table
from misc.Mapper import Mapper


def nw(reader, gap):
    first, second = reader.seqs
    first, second = " " + first, " " + second
    mapper = Mapper(reader.mapper, first, second)

    firstlen = len(first) - 1
    secondlen = len(second) - 1

    F = empty_table(firstlen + 1, secondlen + 1)

    # инициализация первой строки и первого столбца
    for i in range(firstlen + 1):
        F[i][0] = gap * i
    for i in range(secondlen + 1):
        F[0][i] = gap * i

    # заполнение матрицы
    # выбирается максимальный элемент из предыдущих
    for i in range(1, firstlen + 1):
        for j in range(1, secondlen + 1):
            match = F[i - 1][j - 1] + mapper(i, j)
            insert = F[i - 1][j] + gap
            delete = F[i][j - 1] + gap
            maximum = max(match, delete, insert)
            F[i][j] = maximum

    # начиная с последей клетки восстанавливаем последовательности
    A = ""
    B = ""
    i = firstlen
    j = secondlen
    while i > 0 and j > 0:
        score = F[i][j]
        diag = F[i - 1][j - 1]
        up = F[i - 1][j]
        left = F[i][j - 1]
        # если пришли с диагонали, то совпадение
        if score == diag + mapper(i, j):
            A = first[i] + A
            B = second[j] + B
            i -= 1
            j -= 1
        #пришли слева - делеция
        elif score == left + gap:
            A = "-" + A
            B = second[j] + B
            j -= 1
        #пришли сверху - инсерция
        elif score == up + gap:
            A = first[i] + A
            B = "-" + B
            i -= 1

    # заполняем гэпами начала строк
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
    reader.output(A, B, F[firstlen][secondlen])
    return A, B, F[firstlen][secondlen], first, second


def nw_affine(reader, opengap, extended=-1):
    first, second = reader.seqs
    first, second = " " + first, " " + second
    mapper = Mapper(reader.mapper, first, second)

    firstlen = len(first) - 1
    secondlen = len(second) - 1

    # используем несколько матриц вместе с матрицей направлений
    M = empty_table(firstlen + 1, secondlen + 1)
    In = empty_table(firstlen + 1, secondlen + 1)
    D = empty_table(firstlen + 1, secondlen + 1)
    R = empty_table(firstlen + 1, secondlen + 1)


    # задаем значение бесконечности для инициализации матрицы
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

    # заполняем несколько матриц
    for i in range(1, firstlen + 1):
        for j in range(1, secondlen + 1):
            M[i][j] = max(M[i - 1][j - 1] + mapper(i, j), In[i - 1][j - 1] + mapper(i, j),
                          D[i - 1][j - 1] + mapper(i, j))
            D[i][j] = max(D[i][j - 1] + extended, M[i][j - 1] + opengap, In[i][j - 1] + opengap)
            In[i][j] = max(In[i - 1][j] + extended, M[i - 1][j] + opengap, In[i - 1][j] + opengap)

    # выбираем направление по которому идем в зависимости от
    # максимального элемента из трех матриц в данной позиции
    for i in range(firstlen + 1):
        for j in range(secondlen + 1):
            R[i][j] = max((In[i][j], 2), (D[i][j], 1),  (M[i][j], 0))

    # восстановление выравнивания
    A = ""
    B = ""
    i = firstlen
    j = secondlen
    while i > 0 and j > 0:
        direction = R[i][j][1]
        # если максимальный элемент из матрицы М то идем по диагонали
        if direction == 0:
            A = first[i] + A
            B = second[j] + B
            i -= 1
            j -= 1
        #     если из матрицы D то идем влево ( делеция )
        elif direction == 1:
            A = "-" + A
            B = second[j] + B
            j -= 1
        #     если из матрицы In то идем вверх ( инсерция )
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
