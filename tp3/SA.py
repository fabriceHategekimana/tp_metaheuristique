from module import TaskDefinitionFile, Path, read_city, get_energy_generator
from collections.abc import Callable
import numpy as np
import random
import sys
import attr


@attr.s
class EquilibrumRecord:
    accepted_perturbations: int = attr.ib(default=0)
    tentatives: int = attr.ib(default=0)
    n: int = attr.ib(default=0)

    def new_tentative(self):
        self.tentatives += 1

    def accepted(self):
        self.accepted_perturbations += 1


class TemperatureRecord:
    record: list[float] = [0, 0]

    def __init__(self, initial_temperature: float):
        self.record.append(initial_temperature)

    def push(self, temperature):
        self.record.pop(0)
        self.record.append(temperature)

    def get_record(self):
        return self.record.copy()


def generate_randint_tuple(n: int):
    r1 = random.randint(0, n-1)
    r2 = random.randint(0, n-1)
    while r1 == r2:
        r2 = random.randint(0, n-1)
    return r1, r2


def switch_path(path: Path, n: int) -> Path:
    # permute path
    for i in range(n):
        r1, r2 = generate_randint_tuple(len(path))
        path[r1], path[r2] = path[r2], path[r1]
    return path


def generate_path(uncycled_path: list[str]) -> Path:
    random.shuffle(uncycled_path)
    return uncycled_path


def diff_path(path: Path, get_energy: Callable) -> int:
    new_path = switch_path(path.copy(), 100)
    return np.abs(get_energy(new_path)-get_energy(path))


def generate_temperature(path: Path, get_energy: Callable) -> int:
    return -(diff_path(path, get_energy))/np.log(0.5)  # apply natural logarithm


def frozen(temperature_record: TemperatureRecord) -> bool:
    [x, y, z] = temperature_record.get_record()
    return (x == y) and (y == z)


def equilibrum(record: EquilibrumRecord) -> bool:
    return ((record.accepted_perturbations >= (12 * record.n))
            and (record.tentatives >= (100 * record.n)))


def update(path: Path) -> Path:
    return switch_path(path.copy(), 1)


def metropolis_rule(energy: float, temperature: float):
    return 1.0 if energy < 0 else np.exp((-energy)/temperature)


def acceptance(old_path: Path, new_path: Path, temperature: float, new_temperature: float, equilibrum_record: EquilibrumRecord) -> Path:
    equilibrum_record.new_tentative()
    res = random.random() > metropolis_rule(new_temperature, temperature)
    if res:
        equilibrum_record.accepted()
    return res


def simulated_annealing(file: TaskDefinitionFile) -> tuple[Path, int]:
    path, cities = read_city(file)
    get_energy = get_energy_generator(cities)
    path = generate_path(path)  # random
    temperature = generate_temperature(path, get_energy)  # see initial temperature equation
    temperature_record = TemperatureRecord(temperature)
    equilibrum_record = EquilibrumRecord(0, 0, len(cities))
    while not frozen(temperature_record):
        while equilibrum(equilibrum_record):
            new_path = update(path)  # random permutation
            new_temperature = get_energy(new_path)
            temperature_record.push(new_temperature)
            new_path = acceptance(path, new_path, temperature, new_temperature, equilibrum_record)
            temperature = new_temperature
    return path, get_energy(path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("You should specify the file name")
    res = simulated_annealing(sys.argv[1])
    print("res:", res)

# TODO : faire en sorte à ce que'un chemin commence et fini par la même ville
# TODO : implémenter la version greedy
# TODO : checker simulated_annealing() ligne par ligne
