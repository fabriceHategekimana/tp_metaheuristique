from typing import Callable
import random


def do_equal(val1, val2):
    if val1 is None or val2 is None:
        return 0
    else:
        return val1 == val2


# This is the machine on which programs are executed
# The output is the value on top of the pile.
class CPU:
    def __init__(self):
        self.pile: list[int] = []

    def reset(self):
        while len(self.pile) > 0:
            self.pile.pop()

    def push(self, val: int):
        self.pile.append(val)

    def pop(self) -> int | None:
        return self.pile.pop() if len(self.pile) > 0 else None


# These are the instructions
def AND(cpu: CPU, data: list[int]):
    v1 = cpu.pop()
    v2 = cpu.pop()
    if v1 is not None and v2 is not None:
        v1i: int = v1
        v2i: int = v2
        cpu.push(v1i and v2i)


def OR(cpu: CPU, data: list[int]):
    v1 = cpu.pop()
    v2 = cpu.pop()
    if v1 is not None and v2 is not None:
        v1i: int = v1
        v2i: int = v2
        cpu.push(v1i or v2i)


def XOR(cpu: CPU, data: list[int]):
    v1 = cpu.pop()
    v2 = cpu.pop()
    cpu.push((v1 and v2) or (not (v1 or v2)))


def NOT(cpu: CPU, data: list[int]):
    v = cpu.pop()
    cpu.push(not v)


# Push values of variables on the stack.
def X1(cpu: CPU, data: list[int]):
    cpu.push(data[0])


def X2(cpu: CPU, data: list[int]):
    cpu.push(data[1])


def X3(cpu: CPU, data: list[int]):
    cpu.push(data[2])


def X4(cpu: CPU, data: list[int]):
    cpu.push(data[3])


# Execute a program
def execute(program: list[str], cpu: CPU, data: list[int]) -> int | None:
    for cmd in program:
        CALLS[cmd](cpu, data)
    return cpu.pop()


# Generate a random program
def randomProg(length: int, functionSet: list[str], terminalSet: list[str]) -> list[str]:
    return [random.choice(functionSet+terminalSet) for i in range(length)]


# Computes the fitness of a program.
# The fitness counts how many instances of data in dataSet are correctly
# computed by the program
def computeFitness(prog: list[str], cpu: CPU, dataSet: list[list[int]]) -> int:
    return sum([do_equal(execute(prog, cpu, line[:-1]), line[-1])
                for line in dataSet])


# Selection using 2-tournament.
def selection(Population, cpu: CPU, dataSet):
    listOfFitness = []
    for i in range(len(Population)):
        prog = Population[i]
        f = computeFitness(prog, cpu, dataSet)
        listOfFitness.append((i, f))

    newPopulation = []
    n = len(Population)
    for i in range(n):
        i1 = random.randint(0, n - 1)
        i2 = random.randint(0, n - 1)
        if listOfFitness[i1][1] > listOfFitness[i2][1]:
            newPopulation.append(Population[i1])
        else:
            newPopulation.append(Population[i2])
    return newPopulation


def crossover(Population, p_c):
    newPopulation = []
    n = len(Population)
    i = 0
    while i < n:
        p1 = Population[i]
        p2 = Population[(i + 1) % n]
        m = len(p1)
        if random.random() < p_c:  # crossover
            k = random.randint(1, m - 1)
            newP1 = p1[0:k] + p2[k:m]
            newP2 = p2[0:k] + p1[k:m]
            p1 = newP1
            p2 = newP2
        newPopulation.append(p1)
        newPopulation.append(p2)
        i += 2
    return newPopulation


def mutation(Population, p_m, terminalSet, functionSet):
    newPopulation = []
    nT = len(terminalSet) - 1
    nF = len(functionSet) - 1
    for p in Population:
        for i in range(len(p)):
            if random.random() > p_m:
                continue
            if random.random() < 0.5:
                p[i] = terminalSet[random.randint(0, nT)]
            else:
                p[i] = functionSet[random.randint(0, nF)]
        newPopulation.append(p)
    return newPopulation


CALLS: dict[str, Callable] = {"AND": AND, "OR": OR,
                              "XOR": XOR, "NOT": NOT,
                              "X1": X1, "X2": X2,
                              "X3": X3, "X4": X4}

# -------------------------------------

# LOOK-UP TABLE YOU HAVE TO REPRODUCE.
nbVar = 4
dataSet: list[list[int]] = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0],
]

cpu: CPU = CPU()

# Function and terminal sets.
functionSet: list[str] = ["AND", "OR", "NOT", "XOR"]
terminalSet: list[str] = ["X1", "X2", "X3", "X4"]

# Example of program.
prog: list[str] = ["X1", "X2", "AND", "X3", "OR"]
progLength: int = 5
# Generator
prog = randomProg(progLength, functionSet, terminalSet)

# fitness
print(prog)

# Execute a program on one row of the data set.
data: list[int] = dataSet[0]
output: int | None = execute(prog, cpu, data)
print(output)
print("-------------")

# Parameters
# popSize = None  # TODO
# p_c = None  # TODO
# p_m = None  # TODO
# Generate the initial population
# Evolution. Loop on the creation of population at generation i+1 from population at generation i, through selection, crossover and mutation.

# TODO
# generate a population
prog = randomProg(progLength, functionSet, terminalSet)

# calcule le fitness
score = computeFitness(prog, cpu, dataSet)

# selectionne les survivants


# crossover les parents
# mutation
