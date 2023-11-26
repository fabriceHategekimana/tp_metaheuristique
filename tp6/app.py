import numpy as np
import pandas as pd


def initial_values(size):
    return np.random.choice([0, 1], size=size)


def fitness(x):
    return 1


def get_survivors(df):
    return df


def crossover(row):
    return row


def selection(df, algo):
    return algo(df)


def get_mate(individuals):
    # TODO: I don't know how to get mate together
    # So I will only do a simple coupling
    return pd.DataFrame([individuals[::2], individuals[1::2]],
                        columns=["individual1", "individual2"])


def mutation(params):
    pass


def choose5(individuals):
    pass


def get_best(candidate):
    pass


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
        df["fitness"] = df["individual"].apply(fitness)
        mates = (get_mate(selection(df, tournament5(N//2)))
                 .apply(crossover, axis=1))
        df = pd.DataFrame((mates["individual1"] + mates["individual2"])
                          .apply(mutation), columns=["individual"])
    return df


if __name__ == '__main__':
    res = genetic_algorithm(1, 3, 1)
    print("res:", res)
