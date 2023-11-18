from task_definition_manager import get_cities
from core import mymap
import pandas as pd
import numpy as np
import random

from task_definition_manager import save_file
from task_definition_manager import open_file


def cross_product(list_of_value):
    return np.array([(x, y) for x in list_of_value for y in list_of_value])


def get_coordinates(df, name):
    return np.array(df.query(f"name == '{name}'").iloc[0])[1:]


def compute_distance(setting, c1, c2):
    coords1 = get_coordinates(setting, c1)
    coords2 = get_coordinates(setting, c2)
    return np.linalg.norm(coords2 - coords1)


def compute_distances(setting: pd.DataFrame) -> pd.DataFrame:
    """compute the distances
    between all points of a setting (coordinates of cities)"""
    cities = get_cities(setting)
    couples_of_cities = cross_product(cities)
    c1_c2_distances = mymap(
        lambda c: compute_distance(setting, c[0], c[1]), couples_of_cities
    )
    dataframe = {
        "c1": couples_of_cities[:, 0],
        "c2": couples_of_cities[:, 1],
        "distance": c1_c2_distances,
    }
    return pd.DataFrame(dataframe)


def get_distance(distances, c1, c2):
    return tuple(distances.query(f"c1 == '{c1}' and c2 == '{c2}'").iloc[0])[-1]


def compute_fitness(combination: list[str], dist: pd.DataFrame) -> int:
    """compute path length of a combination (of cities)"""
    combination_extended = combination.copy() + [combination[0]]
    couples = mymap(
        lambda i: [combination_extended[i], combination_extended[i + 1]],
        range(len(combination_extended) - 1),
    )
    distances = mymap(lambda c: get_distance(dist, c[0], c[1]), couples)
    return np.sum(distances)


def tau(T, i, j):
    return get_pheromone(T, i, j)


def prob_to_city(i, j, J, dist, T, alpha, beta):
    """compute the probability of moving from city i to city j (j belongs to J)"""
    if j in J:
        up = (tau(T, i, j)) ** alpha * (eta(dist, i, j)) ** beta
        down = sum(
            mymap(lambda la: tau(T, i, la) ** alpha * (eta(dist, i, la) ** beta), J)
        )
        return up / down
    else:
        return 0


def get_pheromone(T, i, j):
    return tuple(T.query(f"c1 == '{i}' and c2 == '{j}'").iloc[0])[-1]


def eta(dist, i, j):
    return 1 / get_distance(dist, i, j)


def ant_path(setting, dist, T, alpha, beta, J):
    """
    path of each individual ant (out of m ants)
    this function can be parallelized and used later in the main AS function
    setting: DataFrame["name", ]
    dist: DataFrame["city1", "city2", "dist"]
    """
    cities = sorted(get_cities(setting))
    random_index = random.randint(0, len(cities) - 1)
    city = cities.pop(random_index)
    explored = [city]
    while len(cities) > 0:
        # coords = mymap(lambda c: get_coordinates(setting, c), cities)
        probabilities = mymap(
            lambda c: prob_to_city(city, c, J, dist, T, alpha, beta), cities
        )
        # TODO use random sample
        next_city = cities[np.argmax(probabilities)]
        cities.remove(next_city)
        explored.append(next_city)
    return explored, compute_fitness(explored, dist)
