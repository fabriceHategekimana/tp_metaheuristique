import matplotlib.pyplot as plt
from itertools import dropwhile
import numpy as np
import pandas as pd
import random

INDIVIDUAL1 = "individual1"
INDIVIDUAL2 = "individual2"


def visualize(f, interval, points=100):
    x = np.linspace(interval[0], interval[1], points)
    y = np.linspace(interval[0], interval[1], points)
    x, y = np.meshgrid(x, y)
    z = f(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='viridis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def fxy(x, y):
    '''
    returns result of function f(x, y) which we are trying to minimize

    Parameters:
    -----------
    x : x-coordinate of point (can be an array of x-coordinates)
    y : y-coordinate of point (can be an array of y-coordinates)

    Returns:
    --------
    result f(x, y) (can be an array of function evaluations)
    '''
    first = np.abs(0.5*x*np.sin(np.sqrt(np.abs(x))))
    second = np.abs(y*np.sin(30*np.sqrt(np.abs(x/y))))
    return - first - second


def to_decimal(binary_string):
    res = int(binary_string, 2)
    if res < 10:
        res = 10
    elif res > 1000:
        res = 1000
    return res


def mapping(binary_string):
    return to_decimal(binary_string[:10]), to_decimal(binary_string[10:])


def to_10bits(n):
    if n < 10 or n > 1000:
        raise ValueError("Le nombre doit être compris entre 0 et 1023 inclus.")
    binary_representation = bin(n)[2:]
    padded_binary = binary_representation.zfill(10)
    return padded_binary


def to_bits_coordinates(coords):
    return to_10bits(coords[0]) + to_10bits(coords[1])


def initial_values(size):
    return "".join([str(i) for i in np.random.choice([0, 1], size=size)])


def ftuple(f):
    return lambda t: f(t[0], t[1])


def calculate_fitness(f, gen):
    '''
    calculates the fitness of one element generation

    Parameters:
    -----------
    gen : generation of N individuals of k-bits each
    k : binary x-y coordinate size

    Returns:
    --------
    g_fitness : fitness of generation
    (fitness for each individual in the N population)
    '''
    x, y = mapping(gen)
    return f(x, y)


def map_xy(xy, length, a, b):
    '''
    maps binary string to natural number in range of natural numbers [a, b]

    Parameters:
    -----------
    xy : binary string, x or y coordinate to be mapped
         to a natural number in range [a, b]
    length : length of string
    a : lower range limit
    b : upper range limit

    Returns:
    --------
    integer value in the range [a, b]
    '''


def crossover(pc):
    def crossover_helper(row):
        if np.random.rand() > pc:
            parent1, parent2 = row[INDIVIDUAL1], row[INDIVIDUAL2]
            point = random.randint(0, len(parent1)-1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return pd.Series({INDIVIDUAL1: child1, INDIVIDUAL2: child2})
        else:
            return row
    return crossover_helper


def get_mate(individuals):
    return pd.DataFrame({INDIVIDUAL1: individuals[::2],
                         INDIVIDUAL2: individuals[1::2]})


def mutation(pm):
    def mutation_helper(gen):
        '''
        performs mutation to each individual in generation gen
        (with a probability m_p for every individual,
        decide to swap every element of an individual 0->1 or 1->0)

        Parameters:
        -----------
        gen : generation of N individuals of k-bits each
        p_m : probability of mutation

        Returns:
        --------
        gen: generation gen after mutation process
        '''
        point = random.randint(0, len(gen)-1)
        gen = list(gen)
        if np.random.rand() > pm:
            gen[point] = "1" if gen[point] == "0" else "0"
        return "".join(gen)
    return mutation_helper


def probabilistic_choice(candidates):
    probabilities = [num / sum(candidates) for num in candidates]
    random_value = random.uniform(0, 1)
    return list(dropwhile(lambda i: sum(probabilities[:i+1]) <= random_value,
                          range(len(probabilities))))[0]


def choose5(individuals):
    return [random.choice(list(individuals)) for i in range(5)]


def get_best(candidates, f):
    index = probabilistic_choice([calculate_fitness(f, c) for c in candidates])
    return candidates[index]


def tournament5_helper(individuals, f):
    candidates = choose5(individuals)
    best = get_best(candidates, f)
    return best


def tournament5(gen, N, f):
    '''
    performs 5-Tournament Selection on generation
    (choose 5 random individuals,
    return the best one in terms of fitness, repeat process N times)

    Parameters:
    -----------
    gen : generation of N individuals of k-bits each
    N : population size

    Returns:
    --------
    gen : generation gen after selection process

    NOTE: remember to repeat selection process N times to keep
          a constant population size
    '''
    return [tournament5_helper(gen, f) for n in range(N)]


def generate_gen(N, k):
    '''
    generates N populations of k-bits each
    (first k/2 bits are x binary coordinates,
    and second k/2 bits are y-binary coordinates)

    Parameters:
    -----------
    N : population size
    k : binary x-y coordinate size

    Returns:
    --------
    gen : generation of N individuals of k-bits each
    '''
    return pd.DataFrame([initial_values(k) for i in range(N)],
                        columns=["individual"])


def GA(N, k, p_c, p_m, evals, crossOver=True, track_best=True, f=fxy):
    '''
    performs Genetic Algorithm
    (choose number of iterations depending on number of
    evaluations needed where :
    num_evaluations = population_size * num_iterations)

    Parameters:
    -----------
    N : population size
    k : size of individual (length of bit string)
    p_c : probability of crossover
    p_m : probability of mutation
    evals : number of evaluations
    crossOver : =True to perform crossover, & False otherwise
    track_best : =True to keep track of best seen so far for each individual,
    & False otherwise
    f : the f(x, y) function to work on

    Returns:
    --------
    gen : generation gen after number of evaluations
    g_fitness : generations fitness (N fitnesses)
    fit_best : best so far for each individual
    (list of zeros in case track_best=False)
    probs : list of empirical probabilities (relative frequencies),
    of individuals reaching optimum, at each iteration
    probs1 : list of empirical probabilities (relative frequencies),
    of individuals at most 1% away from optimum, at each iteration
    probs2p5 : list of empirical probabilities (relative frequencies),
    of individuals at most 2.5% away from optimum, at each iteration
    '''
    # generate a population of N individuals, of k-bit strings each
    gen = generate_gen(N, k)

    # fit_best : to update in case of track_best=True
    fit_best = "1"*k
    # list of empirical probabilities (relative frequencies),
    # of individuals reaching optimum, at each iteration
    probs = []
    # list of empirical probabilities (relative frequencies),
    # of individuals reaching at most 1% away from optimum, at each iteration
    probs1 = []
    # list of empirical probabilities (relative frequencies),
    # of individuals reaching at most 2.5% away from optimum, at each iteration
    probs2p5 = []

    g_fitness = []

    # number of iterations can be calculated from:
    # num_evaluations = population_size * num_iterations
    iterations = evals//len(gen)
    fitnesses = None
    best_index = 0
    for _ in range(iterations):
        # selection
        # df["fitness"] = df["individual"].apply(calculate_fitness)
        mates = get_mate(tournament5(gen["individual"], N, f))
        # crossover (if True)
        childs = mates.apply(crossover(p_c), axis=1)
        gen = pd.concat([childs, mates], ignore_index=True)
        # mutation
        gen = pd.DataFrame(pd.Series(list(gen[INDIVIDUAL1]) + list(gen[INDIVIDUAL2]))
                           .apply(mutation(p_m)), columns=["individual"])
        fitnesses = gen.apply(lambda x: calculate_fitness(f, x["individual"]),
                              axis=1)
        g_fitness.append(fitnesses.mean())
        if track_best:
            # append empirical probabilities depending
            # on keeping track of best or not
            # get fitness
            best_index = probabilistic_choice([calculate_fitness(f, c)
                                               for c in list(gen["individual"])])
            if fitnesses[best_index] > calculate_fitness(f, fit_best):
                fit_best = gen["individual"][best_index]
    gen["fitness"] = fitnesses
    probs = len(gen[gen["fitness"] >= fitnesses[best_index]]) / len(gen)
    probs1 = len(gen[gen["fitness"] >= (fitnesses[best_index]*99)/100]) / len(gen)
    probs2p5 = len(gen[gen["fitness"] >= (fitnesses[best_index]*97.5)/100]) / len(gen)
    return gen, g_fitness, fit_best, probs, probs1, probs2p5


def my_f(x, y):
    return - ((x ** 2) + (y ** 2))


if __name__ == '__main__':
    res = GA(N=6, k=20, p_c=0.1, p_m=0, evals=24,
             crossOver=True, track_best=True, f=my_f)
    df, g_fitness, fit_best, probs, probs1, probs2p5 = res
    print("df:", df)
    print("g_fitness:", g_fitness)
    print("fit_best:", fit_best)
    print("probs:", probs)
    print("probs1:", probs1)
    print("probs2q5:", probs2p5)
