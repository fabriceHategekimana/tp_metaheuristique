TaskDefinitionFile = str
Path = list[str]  # same city at the beginning and at the end
Cities = dict[str, tuple[float, float]]


def read_city(file: TaskDefinitionFile) -> tuple[Path, Cities]:
    f = open(file)
    extracted_cities = [x.replace("\n", "").split(" ") for x in f.readlines()]
    f.close()
    cities_dict = {city: (float(x), float(y)) for [city, x, y] in extracted_cities}
    path = [city for [city, x, y] in extracted_cities]
    return path, cities_dict


# got:
# Tuple[List[str], Dict[str, Tuple[float, float]]]
# expected:
# Tuple[List[str], Dict[str, Tuple[int, int]]]
