from module import TaskDefinitionFile, Path, read_city, Cities
import numpy as np
import random
import sys
import attr


@attr.s
class EquilibrumRecord:
    accepted_perturbations: int = attr.ib(default=0)
    tentatives: int = attr.ib(default=0)
    n: int


def get_energy(path: Path) -> int:
    return len(path)


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


def diff_path(path: Path) -> int:
    new_path = switch_path(path.copy(), 100)
    return np.abs(get_energy(new_path)-get_energy(path))


def generate_temperature(path: Path) -> int:
    return -(diff_path(path))/np.log(0.5)  # apply natural logarithm


def frozen(temperature_record: list[float]) -> bool:
    [x, y, z] = temperature_record
    return (x == y) and (y == z)


def equilibrum(record: EquilibrumRecord) -> bool:
    return ((record.accepted_perturbations >= (12 * record.n))
            and (record.tentatives >= (100 * record.n)))


def update(path: Path) -> Path:
    return switch_path(path.copy())


def metropolis_rule(energy: float, temperature: float):
    return 1.0 if energy < 0 else np.exp((-energy)/temperature)


def acceptance(old_path: Path, new_path: Path, temperature: float) -> Path:
    return random.random() > metropolis_rule(energy, temperature)


def simulated_annealing(file: TaskDefinitionFile) -> tuple[Path, int]:
    path, cities = read_city(file)
    path = generate_path(path)  # random
    temperature = generate_temperature(path)  # see initial temperature equation
    temperature_record = [0, 0, temperature]
    equilibrum_record = EquilibrumRecord(0, 0, len(cities))
    while not frozen(temperature_record):
        while equilibrum(equilibrum_record):
            new_path = update(path)  # random permutation
            new_path = acceptance(path, new_path, get_energy(new_path), temperature)
    return path, len(path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("You should specify the file name")
    simulated_annealing(sys.argv[1])
