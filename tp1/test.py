import unittest
from module import generate_sequence, compute_fitness, neighbors, deterministic_hillclimb, probabilistic_hillclimb, hamming_distance
import numpy as np


class name(unittest.TestCase):

    # be sure to use the prefix "test_"
    def test_generator(self):
        seq = generate_sequence(10)
        assert len(seq) == 10
        assert np.sum(np.sort(np.unique(seq)) - np.array([0, 1])) == 0

    def test_global_fitness(self):
        sequence1 = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        sequence2 = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        table = {1: {"00": -1, "01": 1, "10": 1, "11": -1}}
        res1 = compute_fitness(sequence1, K=1, table=table)
        res2 = compute_fitness(sequence2, K=1, table=table)
        assert res1 == res2

    def test_neighbors(self):
        neigh = neighbors(np.array([0, 1]))
        assert (neigh-np.array([[1, 1], [0, 0]])).sum() == 0

    def test_deterministic_hillclimb(self):
        deterministic_hillclimb(np.array([0, 1]), 0)
        assert True

    def test_probabilistic_hillclimb(self):
        probabilistic_hillclimb(np.array([0, 1]), 0)
        assert True

    def test_hamming_distance(self):
        s1 = np.array([1, 0, 1])
        s2 = np.array([0, 0, 1])
        assert hamming_distance(s1, s2) == 1


if __name__ == '__main__':
    unittest.main()
