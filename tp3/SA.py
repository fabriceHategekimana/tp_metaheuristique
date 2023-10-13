from module import TaskDefinitionFile, Path, read_city


def get_energy(path: Path) -> int:
    return len(path)


def simulated_annealing(file: TaskDefinitionFile) -> tuple[Path, int]:
    cities = read_city(file)
    path = generate_path(cities)  # random
    temperature = generate_temperatur(cities) # see initial temperature equation
    while not frozen():
        while equilibrum():
            new_path = update(path)  # random permutation
            new_path = acceptance(new_path, temperature)
    return path
