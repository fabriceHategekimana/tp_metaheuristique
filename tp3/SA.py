from module import TaskDefinitionFile, Path, read_city, get_energy_generator, Temperature, Energy
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


class EnergyRecord:
    record: list[float] = [0]

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


def generate_temperature(path: Path, get_energy: Callable) -> Temperature:
    return -(diff_path(path, get_energy))/np.log(0.5)  # apply natural logarithm


def generate_frozen(get_energy):
    energy_record = EnergyRecord()

    def delta_energy(new_path, old_path):
        d_energy = get_energy(new_path) - get_energy(path)
        energy_record.push(d_energy)
        return d_energy

    def frozen() -> bool:
        [x, y, z] = energy_record.get_record()
        return (x == y) and (y == z)
    return energy_record, frozen, delta_energy




def update(path: Path) -> Path:
    return switch_path(path.copy(), 1)


def metropolis_rule(energy: Energy, temperature: Temperature):
    return 1.0 if energy < 0 else np.exp((-energy)/temperature)


def generate_acceptance():
    record = EquilibrumRecord()

    def acceptance(old_path: Path, new_path: Path, temperature: float, energy: float):
        record.new_tentative()
        res: bool = random.random() > metropolis_rule(energy, temperature)
        if res:
            record.accepted()
            return new_path
        else:
            return old_path

    def equilibrum() -> bool:
        return ((record.accepted_perturbations >= (12 * record.n))
                or (record.tentatives >= (100 * record.n)))
    return record, equilibrum, acceptance


def initial_configuration(file):
    path, cities = read_city(file)
    path = generate_path(path)
    get_energy = get_energy_generator(cities)
    return path, cities, get_energy


def initial_temperature(path: Path, get_energy: Callable):
    return generate_temperature(path, get_energy)


def initial_functions(equilibrum_record, temperature_record):
    acceptance = generate_acceptance(equilibrum_record)
    frozen = generate_frozen(temperature_record)
    return acceptance, frozen


def simulated_annealing(file: TaskDefinitionFile) -> tuple[Path, int]:
    path, cities, get_energy = initial_configuration(file)
    temperature = initial_temperature(path, get_energy)
    equilibrum_record, equilibrum, acceptance = generate_acceptance()
    energy_record, frozen, delta_energy = generate_frozen(get_energy)
    # while not frozen(temperature_record):
    for i in range(5):
        while not equilibrum():
            print("equilibrum:", equilibrum_record)
            print("temperature:", temperature)
            new_path = update(path)  # random permutation
            d_energy = delta_energy(new_path, path)
            new_path = acceptance(path, new_path, temperature, d_energy)
            temperature = 0.9 * temperature
    return path, get_energy(path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("You should specify the file name")
    res = simulated_annealing(sys.argv[1])
    print("res:", res)

# TODO : faire en sorte à ce que'un chemin commence et fini par la même ville
# TODO : implémenter la version greedy
# TODO : checker simulated_annealing() ligne par ligne
