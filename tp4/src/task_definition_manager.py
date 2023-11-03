import pandas as pd
from core import mymap, myfilter


def remove_blank_line(triplet):
    return myfilter(lambda x: x != '', triplet)


def open_file(filename):
    ''' data: name of the data :: DataFrame(name, x, y)'''
    text = get_text(filename)
    array_2D = mymap(lambda x: format_cities_columns(x), text)
    df = pd.DataFrame(array_2D, columns=["name", "x", "y"])
    df["x"] = df["x"].astype(float)
    df["y"] = df["y"].astype(float)
    return df


def get_text(filename):
    f = open(filename)
    text = f.read().splitlines()
    f.close()
    return text


def format_cities_columns(string_triplet):
    triplet = string_triplet.split(" ")
    triplet = remove_blank_line(triplet)
    return [triplet[0], float(triplet[1]), float(triplet[2])]


def get_cities(df):
    return list(df["name"])


def save_file(data, file_name):
    with open(f"{file_name}.dat", "w") as file:
        for name, x, y in zip(data["name"], data["x"], data["y"]):
            line = f"{name} {x} {y}"
            file.write(line)
