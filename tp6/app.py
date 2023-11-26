import numpy as np
import pandas as pd
import random


def initial_values(size):
    return np.random.choice([0, 1], size=size)


def mapping(a, b):
    # m number of bits of the sequence
    return lambda x: (x/(2 ** len(x))) * (b-a) + a


def compute_fitness(x):
    return 1


def crossover(row):
    parent1, parent2 = row["individual1"], row["individual2"]
    columns = ["individual1", "individual2"]
    point = random.randint(0, len(parent1)-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return pd.DataFrame([child1, child2], columns=columns)


def selection(df, algo):
    return algo(df)


def get_mate(individuals):
    # TODO: I don't know how to get mate together
    # So I will only do a simple coupling
    return pd.DataFrame([individuals[::2], individuals[1::2]],
                        columns=["individual1", "individual2"])


def mutation(individual):
    point = random.randint(0, len(individual)-1)
    individual[point] = 1 if individual[point] == 0 else 0
    return individual


def choose5(individuals):
    shuffled = random.shuffle(individuals)
    return shuffled[:5], shuffled[5:]


def get_best(candidates):
    fitness = [compute_fitness(c) for c in candidates]
    return sorted(zip(candidates, fitness),
                  key=lambda x: x[1])[0][1]


def tournament5_helper(individuals):
    candidate, rest_individuals = choose5(individuals)
    best, rest_candidates = get_best(candidate)
    return best, (rest_individuals + rest_candidates)


def tournament5(i):
    def fun(df):
        res = []
        rest = df["individual"]
        for n in range(i):
            best, rest = tournament5_helper(rest)
            res.append(best)
        return rest
    return fun


def genetic_algorithm(N, size, G):
    df = pd.DataFrame([initial_values(size).__str__() for i in range(N)],
                      columns=["individual"])
    for i in range(G):
        df["fitness"] = df["individual"].apply(compute_fitness)
        mates = get_mate(selection(df, tournament5(N//2)))
        childs = mates.apply(crossover, axis=1)
        df = pd.concat([mates, childs], ignore_index=True)
        df = pd.DataFrame((df["individual1"] + df["individual2"])
                          .apply(mutation), columns=["individual"])
    return df


if __name__ == '__main__':
    res = genetic_algorithm(1, 3, 1)
    print("res:", res)
