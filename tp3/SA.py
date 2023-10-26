from module import TaskDefinitionFile, Path, read_city, Cities
import numpy as np
import random
import sys


def get_energy(path: Path) -> int:
    return len(path)


def generate_randint_tuple(n: int):
    r1 = random.randint(0, n)
    r2 = random.randint(0, n)
    while r1 == r2:
        r2 = random.randint(0, n)
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
    return np.abs(new_path-path)


def generate_temperature(path: Path) -> int:
    return -(diff_path(path))/np.log(0.5)  # apply natural logarithm


def frozen() -> bool:
    pass


def equilibrum() -> bool:
    pass


def update(path: Path) -> Path:
    pass


def acceptance(path: Path, temperature: int) -> Path:
    pass


def simulated_annealing(file: TaskDefinitionFile) -> tuple[Path, int]:
    path, cities = read_city(file)
    path = generate_path(path)  # random
    temperature = generate_temperature(path)  # see initial temperature equation
    while not frozen():
        while equilibrum():
            new_path = update(path)  # random permutation
            new_path = acceptance(new_path, temperature)
    return path, len(path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("You should specify the file name")
    simulated_annealing(sys.argv[1])
