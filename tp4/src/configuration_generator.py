import random
from src.module import Cities


def generate_random_dict(n: int) -> Cities:
    random_dict = {}
    for i in range(n):
        key = f'c{i}'
        value = (random.uniform(0, 1), random.uniform(0, 10))
        random_dict[key] = value
    return random_dict


def write_dict_to_file(data_dict: Cities, file_name: str):
    with open(f"{file_name}.dat", "w") as file:
        for key, value in data_dict.items():
            line = f"{key} {value[0]:.4f} {value[1]:.2f}\n"
            file.write(line)


def generate_configuration(file_name: str, cities_number: int = 10):
    random_dictionary = generate_random_dict(cities_number)
    write_dict_to_file(random_dictionary, file_name)
