W = [[0, 1], [1, 2], [2, 3], [0, 2], [1, 3], [0, 3]]


def mymap(function, value_list):
    return list(map(function, value_list))


def myfilter(function, value_list):
    return list(filter(function, value_list))


def cartesian_product(x):
    return [[a, b] for a in x for b in x]


def contains_same_elements(couple):
    return True if couple[0] == couple[1] else False


def unique(input_list):
    res = []
    for el in input_list:
        if el not in res:
            res.append(el)
    return res


def filter_relations(relations):
    filtered_relations = unique(mymap(sorted, relations))
    remove_same = lambda x : not contains_same_elements(x)
    return myfilter(remove_same, filtered_relations)


def to_w(w_coordinates):
    return W.index(w_coordinates)+1


def to_w_coordinates_generator(combination):
    return lambda x: sorted([combination[x[0]], combination[x[1]]])


def get_filtered_relations(combination):
    relations = cartesian_product(combination)
    filtered_relations = sorted(filter_relations(relations))
    return filtered_relations


def psi(combination, relations):
    f = lambda x: [combination[x[0]], combination[x[1]]]
    return mymap(f, relations)


def get_w_tab(combination):
    filtered_relations = get_filtered_relations(combination)
    # create the converter function
    to_w_coordinates = to_w_coordinates_generator(combination)
    wcs = mymap(to_w_coordinates, filtered_relations)
    # print(wcs)
    return wcs
    # ws = mymap(to_w, wcs)
    # print(ws)


def swap_two(combination, i, j):
    '''
    returns a new permutation with facilities in i & j swapped

    Parameters:
    -----------
    combination : list of original facilities' assignment
    i, j : locations of facilities being swapped

    Returns:
    --------
    neighbor : new permutation
    '''
    a = combination.index(i)
    b = combination.index(j)

    combination[a], combination[b] = combination[b], combination[a]
    return combination


def main():
    a = [0, 3, 1, 2, 4]
    print("a:", a)
    get_w_tab(a)

    print("")
    print("-----------------")
    print("")

    b = swap_two(a, 3, 2)
    print("b:", b)
    get_w_tab(b)


# main()

def get_distance(combination):
    relations = get_filtered_relations(combination)
    return sorted(psi(combination, relations))


def main2():
    combination1 = [0, 1, 2, 3]
    d1 = get_distance(combination1)
    combination2 = swap_two(combination1.copy(), 0, 1)
    d2 = get_distance(combination2)
    print("combination1:", combination1)
    print("combination2:", combination2)
    print(d1)
    print(d2)


main2()

# combination1 = [1, 0, 2, 3]
# res = get_filtered_relations(combination1)
# print("res:", res)
# res = get_w_tab(combination1)
# print("res:", res)
