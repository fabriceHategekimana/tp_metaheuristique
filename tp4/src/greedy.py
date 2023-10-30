import numpy as np
from module import compute_distance
from task_definition_manager import open_file


def get_nearest_city(city, path, cities):
    distances = [compute_distance(cities, city, c) for c in path]
    return path[np.argmin(distances)]


def greedy(file: str):
    cities = open_file(file)
    path = list(cities["name"])
    res = []
    city = path.pop(0)
    res.append(city)
    while len(path) > 0:
        nearest_city = get_nearest_city(city, path, cities)
        path.remove(nearest_city)
        res.append(nearest_city)
    return res
