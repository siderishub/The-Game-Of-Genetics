# import matplotlib.pyplot as plt
# plt.rcParams["animation.html"] = "jshtml"
#
# import seagull as sg
# from seagull.lifeforms import Pulsar
#
# # Initialize board
# board = sg.Board(size=(19,60))
#
# # Add three Pulsar lifeforms in various locations
# board.add(Pulsar(), loc=(1,1))
# board.add(Pulsar(), loc=(1,22))
# board.add(Pulsar(), loc=(1,42))
# board.view()
# # Simulate board
# sim = sg.Simulator(board)
# board.view()
# sim.run(sg.rules.conway_classic, iters=1000)
# board.view()
# anim = sim.animate()
# board.view()
# plt.show()

from random import randint, random
from copy import deepcopy

ROWS = 10
COLUMNS = 10
POPULATION = 1000
GENERATIONS = 30
RUN = 7
RAN_PERC = .1

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

def targets(ecosystem):
    return [sum((sum(row) for row in board))**2 for board in ecosystem]

def probabilities(population):
    s = sum(population)
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
        new_population.append(ecosystems[j])
    return new_population



ecosystems = create_ecosystem()

for _ in range(GENERATIONS):
    ecos_copy = deepcopy(ecosystems)
    for _ in range(RUN):
        ecosystems = next_it(ecosystems)

    t = targets(ecosystems)
    p = probabilities(t)
    ecosystems = round_robin(p, ecosystems)


t = targets(ecosystems)
p = probabilities(t)
print(t)
print(max(p))
print(max(t))

example = ecosystems[-1]
pprint(example)
for _ in range(RUN):
    example = next_it([example])[0]
    print()
    pprint(example)