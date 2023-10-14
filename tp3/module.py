TaskDefinitionFile = str
Path = list[str]  # same city at the beginning and at the end
Cities = dict[str, tuple[int, int]]


def read_city(file: TaskDefinitionFile) -> Cities:
    f = open(file)
    extracted_cities = [x.replace("\n", "").split(" ") for x in f.readlines()]
    f.close()
    cities_dict = {city: (x, y) for [city, x, y] in extracted_cities}
    path = [city for [city, x, y] in extracted_cities]
    return path, cities_dict
