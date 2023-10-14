from module import TaskDefinitionFile, Path, read_city, Cities
import random


def get_energy(path: Path) -> int:
    return len(path)


def generate_randint_tuple(n: int):
    r1 = random.randint(0, n)
    r2 = random.randint(0, n)
    while r1 == r2:
        r2 = random.randint(0, n)
    return r1, r2


def switch_path(path: Path, n: int) -> Path:
    for i in range(n):
        r1, r2 = generate_randint_tuple(len(path))
        path[r1], path[r2] = path[r2], path[r1]
    return path


def generate_path(uncycled_path: list[str]) -> Path:
    return random.shuffle(uncycled_path, 1)


def generate_temperature(cities: Cities) -> int:
    return None


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
    temperature = generate_temperature(cities)  # see initial temperature equation
    while not frozen():
        while equilibrum():
            new_path = update(path)  # random permutation
            new_path = acceptance(new_path, temperature)
    return path
