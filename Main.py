from random import randint, random
from copy import deepcopy

ROWS = 9
COLUMNS = 9
POPULATION = 1000
GENERATIONS = 20
RUN = 7
RAN_PERC = 0.15
MUT_PERC = 0.2

def pprint(board):
    for row in board:
        for el in row:
            print(el, end=' ')
        print()


def next_it(ecosystem):
    n = []
    for board in ecosystem:
        copy = [row.copy() for row in board]
        for i, row in enumerate(board):
            for j, el in enumerate(row):
                count = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if not k == l == 0:
                            x = (i+k) % len(board)
                            y = (j+l) % len(board[0])
                            count += board[x][y]
                if el and count not in (2,3):
                    copy[i][j] = 0
                elif not el and count == 3:
                    copy[i][j] = 1
        n.append(copy)
    return n

def create_ecosystem():
    ecosystems = []
    for _ in range(POPULATION):
        ecosystems.append(random_gene())
    return ecosystems

def targets(ecosystems):
    return [sum((sum(row) for row in board))**4 for board in ecosystems]

def BFS(board, pos, bit):
    bit = 1 - bit
    queue = [pos]
    vis = {pos}
    while queue:
        x, y = queue.pop(0)
        if board[x][y] == bit:
            board[x][y] = 1 - board[x][y]
            return
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue

                pos = ((x-i)%ROWS, (y-j)%COLUMNS)
                if pos not in vis:
                    queue.append(pos)
                    vis.add(pos)


def mutation(ecosystem):
    x = randint(0, ROWS-1)
    y = randint(0, COLUMNS-1)

    x2 = randint(0, ROWS-1)
    y2 = randint(0, COLUMNS-1)

    BFS(ecosystem, (x2, y2), ecosystem[x][y])

    ecosystem[x][y] = 1 - ecosystem[x][y]
    return ecosystem


def probabilities(population):
    s = sum(population)
    print('------------------')
    print(s)
    print(max(population))
    return [el/s for el in population]

def random_gene(percent = .15):
    board = []
    for _ in range(ROWS):
        board.append([0 for _ in range(COLUMNS)])

    positions = set()
    l = len(board)
    c = len(board[0])
    for _ in range(round(percent*l*c)):
        x, y = randint(0, l-1), randint(0, c-1)
        while (x, y) in positions:
            x, y = randint(0, l-1), randint(0, c-1)
        positions.add((x, y))
        board[x][y] = 1
    return board


def round_robin(p, ecosystems):
    new_population = []
    for i in range(POPULATION):
        if i < round(POPULATION * RAN_PERC):
            new_population.append(random_gene())
            continue
        sel = random()
        s = p[0]
        j = 0
        while s < sel:
            j += 1
            s += p[j]

        if i < round(POPULATION * RAN_PERC) + round(POPULATION * MUT_PERC):
            new_population.append(mutation(deepcopy(ecosystems[j])))
        else:
            new_population.append(ecosystems[j])
    return new_population



ecosystems = create_ecosystem()

for _ in range(GENERATIONS):
    ecos_copy = deepcopy(ecosystems)
    for _ in range(RUN):
        ecosystems = next_it(ecosystems)

    t = targets(ecosystems)
    p = probabilities(t)
    ecosystems = round_robin(p, ecos_copy)

ecos_copy = deepcopy(ecosystems)
for _ in range(RUN):
    ecosystems = next_it(ecosystems)
t = targets(ecosystems)

example = ecos_copy[t.index(max(t))]
pprint(example)
for _ in range(RUN):
    example = next_it([example])[0]
    print()
    pprint(example)