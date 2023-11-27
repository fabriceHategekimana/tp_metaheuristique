import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


def f(x, y):
    # Question: norm or absolute value
    first = np.abs(0.5*x*np.sin(np.sqrt(np.abs(x))))
    second = np.abs(y*np.sin(30*np.sqrt(np.abs(x/y))))
    return - first - second


def to_decimal(binary_string):
    if len(binary_string) != 10:
        raise ValueError("La chaîne doit avoir une longueur de 10.")
    return int(binary_string, 2)


def mapping(binary_string):
    if len(binary_string) != 20:
        raise ValueError("La chaîne doit avoir une longueur de 20.")
    return to_decimal(binary_string[:10]), to_decimal(binary_string[10:])


def to_10bits(n):
    if n < 10 or n > 1000:
        raise ValueError("Le nombre doit être compris entre 0 et 1023 inclus.")
    binary_representation = bin(n)[2:]
    padded_binary = binary_representation.zfill(10)
    return padded_binary


def to_bits_coordinates(coords):
    return to_10bits(coords[0]) + to_10bits(coords[1])


def initial_values(size):
    return np.random.choice([0, 1], size=size)


def compute_fitness(individual):
    x, y = mapping(individual)
    return f(x, y)


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


def generate_individuals(N, size):
    return pd.DataFrame([initial_values(size).__str__() for i in range(N)],
                        columns=["individual"])


def genetic_algorithm(N, size, G):
    df = generate_individuals(N, size)
    for i in range(G):
        df["fitness"] = df["individual"].apply(compute_fitness)
        mates = get_mate(selection(df, tournament5(N//2)))
        childs = mates.apply(crossover, axis=1)
        df = pd.concat([mates, childs], ignore_index=True)
        df = pd.DataFrame((df["individual1"] + df["individual2"])
                          .apply(mutation), columns=["individual"])
    return df


def visualize(f, interval, points=100):
    x = np.linspace(interval[0], interval[1], points)
    y = np.linspace(interval[0], interval[1], points)
    x, y = np.meshgrid(x, y)
    z = f(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='viridis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


if __name__ == '__main__':
    res = genetic_algorithm(1, 3, 1)
    print("res:", res)
