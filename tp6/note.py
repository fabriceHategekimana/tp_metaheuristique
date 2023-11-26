import itertools
import numpy as np


def mapping(a, b):
    # m number of bits of the sequence
    return lambda x: (x/(2 ** len(x))) * (b-a) + a


def one_point_crossover(params):
    # One point crossover with mid-break policy
    pass


def mutation_operator(pm):
    pass


def run_algo(N):
    # population size
    pass


def f(x, y):
    # Question: norm or absolute value
    first = np.abs(0.5*x*np.sin(np.sqrt(np.abs(x))))
    second = np.abs(y*np.sin(30*np.sqrt(np.abs(x/y))))
    return - first - second


def gen_random_seed():
    pass


# Solution: [x0,..., xN, y0,..., yN]
N = 100
p_m = [0.01, 0.1]
crossover = [None, one_point_crossover]
times = 7

for params in itertools.product(p_m, crossover):
    random_seed = gen_random_seed()
    res = list(map(run_algo(N, params, random_seed), range(10)))
