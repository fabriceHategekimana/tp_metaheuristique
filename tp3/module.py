TaskDefinitionFile = str
Path = list[str]  # same city at the beginning and at the end
Cities = list[list[str]]


def read_city(file: TaskDefinitionFile) -> Cities:
    f = open(file)
    cities = [tuple(x.replace("\n", "").split(" ")) for x in f.readlines()]
    f.close()
    return cities
