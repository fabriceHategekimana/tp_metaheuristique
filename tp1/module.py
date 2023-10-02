import numpy as np
import random


# local fitness functions f_K for K = 0, 1, 2 (Table in TP)
GLOBAL_TABLE = {
    0: {"0": 2, "1": 1},
    1: {"00": 2, "01": 3, "10": 2, "11": 0},
    2: {"000": 0, "001": 1, "010": 1, "011": 0, "100": 2, "101": 0, "110": 0, "111": 0},
}

# -------------------------------------


def generate_sequence(N):
    """
    generates an N random bits (0, 1) sequence

    Parameters:
    -----------
    N : number of bits in the sequence

    Returns:
    --------
    sequence: sequence of N bits
    """
    return np.random.randint(2, size=N)


def local_fitness_generator(table, K):
    def f(seq):
        return table[K]["".join(seq.astype(str))]
    return f


def compute_fitness(sequence, K, table=None):
    """
    computes the fitness of sequence, with respect to K, according to table f

    Parameters:
    -----------
    sequence : N-bits sequence
    K : parameter K (0, 1, or 2)

    Returns:
    --------
    fitness: fitness value of sequence
    """
    table = GLOBAL_TABLE if table is None else table
    local_fitness = local_fitness_generator(table, K)
    # splitted_sequence = np.split(sequence, len(sequence)/(K+1))
    splitted_sequence = np.lib.stride_tricks.sliding_window_view(sequence, K+1)
    return np.apply_along_axis(local_fitness, 1, splitted_sequence).sum()


def neighbors(sequence):
    """
    returns all neighbors of sequence ()

    Parameters:
    -----------
    sequence : N-bits sequence

    Returns:
    --------
    generator of neighbors of sequence
    """

    def switch_at_position(pos):
        seq = sequence.copy()
        seq[pos] = 1 if seq[pos] == 0 else 0
        return np.array(seq)

    # create a list of len(sequence) of sequence
    res = np.array([switch_at_position(x) for x in range(len(sequence))])
    return res


def mean_steps(samples):
    """
    returns mean of steps taken to find solution (for deterministic)

    Parameters:
    -----------
    samples : samples of deterministic_hillclimb runs

    Returns:
    --------
    mean steps
    """
    # get mean of steps needed to find solution (sum of samples' steps/number of samples)
    return sum([x[2]] for x in samples) / len(samples)


def generate_samples(hillclimb_method, K):
    """
    generates 50 samples (solutions) for the hillclimb method (deterministic/probabilistic)

    Parameters:
    -----------
    hillclimb_method : deterministic_hillclimb/probabilistic_hillclimb
    K : parameter K (0, 1, or 2)

    Returns:
    --------
    generator of samples/solutions (sequence, fitness, number of steps)
    """



# -----------------------------


def deterministic_hillclimb(sequence, K):
    """
    performs deterministic_hillclimb

    Parameters:
    -----------
    sequence : N-bits sequence
    K : parameter K (0, 1, or 2)

    Returns:
    --------
    sequence : optimal/fittest sequence found
    max_fitness : fitness value of sequence
    steps: steps it took to reach optimum
    """

    get_fitness = lambda s: compute_fitness(s, K)
    old_sequence = sequence.copy()
    while True:
        neighborhood = neighbors(sequence)
        neighborhood_values = np.apply_along_axis(get_fitness, 1, neighborhood)
        new_sequence = neighborhood[np.argmax(neighborhood_values)]
        if get_fitness(new_sequence) <= get_fitness(old_sequence):
            break
        old_sequence = new_sequence
    return old_sequence


# -----------------------------

def roulette_method(proba_list):
    return lambda: int(list(filter(lambda x: x >= random.random(), np.cumsum(proba_list)))[0])


def probabilistic_hillclimb(sequence, K):
    """
    performs probabilistic_hillclimb

    Parameters:
    -----------
    sequence : N-bits sequence
    K : parameter K (0, 1, or 2)

    Returns:
    --------
    sequence : optimal/fittest sequence found
    max_fitness : fitness value of sequence
    steps: steps corresponding to parameter K
    """
    get_fitness = lambda s: compute_fitness(s, K)
    old_sequence = sequence.copy()
    for step in range(10):
        neighborhood = neighbors(sequence)
        neighborhood_values = np.apply_along_axis(get_fitness, 1, neighborhood)
        new_sequence = neighborhood[np.argmax(neighborhood_values)]
        if get_fitness(new_sequence) <= get_fitness(old_sequence):
            neighborhood_prob = neighborhood_values / neighborhood_values.sum()
            new_sequence = neighborhood[roulette_method(neighborhood_prob)()]
        old_sequence = new_sequence
    return old_sequence


# ---------------------------


def hamming_distance(sequence1, sequence2):
    """
    returns hamming distance between sequence1 and sequence2

    Parameters:
    -----------
    sequence1 : N-bits sequence
    sequence2 : N-bits sequence

    Returns:
    --------
    distance : hamming distance between sequence1 and sequence2
    """
    return np.count_nonzero(sequence1 != sequence2)

