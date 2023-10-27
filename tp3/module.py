from collections.abc import Callable
from functools import reduce
import numpy as np

TaskDefinitionFile = str
Path = list[str]  # same city at the beginning and at the end
Cities = dict[str, tuple[float, float]]
Temperature = float
Energy = float


def distance(cityA: str, cityB: str, cities: Cities) -> float:
    pA = np.array(cities[cityA])
    pB = np.array(cities[cityB])
    return float(np.linalg.norm(pA-pB))


def get_distance(acc: tuple[float, str], y: str, cities: Cities) -> tuple[float, str]:
    return (acc[0] + distance(acc[1], y, cities), y)


def get_energy_generator(cities: Cities) -> Callable:
    def get_energy(path: Path) -> Energy:
        p = list(path)
        return reduce(lambda acc, y: get_distance(acc, y, cities),
                      p[1:]+[p[0]], (0.0, p[0]))[0]
    return get_energy


def read_city(file: TaskDefinitionFile) -> tuple[Path, Cities]:
    f = open(file)
    extracted_cities = [x.replace("\n", "").split(" ") for x in f.readlines()]
    f.close()
    cities_dict = {city: (float(x), float(y)) for [city, x, y] in extracted_cities}
    path = [city for [city, x, y] in extracted_cities]
    return path, cities_dict
