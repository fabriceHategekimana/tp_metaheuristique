from core import *


def generate_task_definition_file(name, sample):
    f = open(name, "a")
    for i in range(1, sample+1):
        if i < sample:
            f.write(f"c{i} {random.random()} {random.random()}\n")
        else:
            f.write(f"c{i} {random.random()} {random.random()}")
    f.close()


def open_file(filename):
    '''
    read .dat file and return a Dataframe(name, x, y)

    Parameters:
    -----------
    filename

    Returns:
    --------
    data: name of the data :: DataFrame(name, x, y)
    '''
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


def remove_blank_line(triplet):
    return myfilter(lambda x: x != '', triplet)


def get_cities(df):
    return list(df["name"])
