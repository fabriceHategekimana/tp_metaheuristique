import numpy as np
from module import compute_distance, compute_fitness
from task_definition_manager import open_file
import random
import time


def get_nearest_city(city, path, cities):
    distances = [compute_distance(cities, city, c) for c in path]
    return path[np.argmin(distances)]


def greedy(file: str):
    cities = open_file(file)
    path = list(cities["name"])
    res = []
    random_index = random.randint(0, len(path)-1)
    city = path.pop(random_index)
    res.append(city)
    while len(path) > 0:
        nearest_city = get_nearest_city(city, path, cities)
        path.remove(nearest_city)
        res.append(nearest_city)
    return res


def find_greedy(setting, dist):
    start = time.time()
    cities = setting
    path = list(cities["name"])
    res = []
    random_index = random.randint(0, len(path)-1)
    city = path.pop(random_index)
    res.append(city)
    while len(path) > 0:
        nearest_city = get_nearest_city(city, path, cities)
        path.remove(nearest_city)
        res.append(nearest_city)
    end = time.time()
    return res, compute_fitness(res, dist), end-start
