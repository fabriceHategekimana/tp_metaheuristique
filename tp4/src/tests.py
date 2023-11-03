import unittest
import numpy as np
from module import (get_coordinates, cross_product,
                    compute_distances, get_distance,
                    compute_fitness, prob_to_city)
from task_definition_manager import open_file
from greedy import greedy


class AS_test(unittest.TestCase):

    file_name = "src/data/cities.dat"

    # be sure to use the prefix "test_"
    def test_coodinates(self):
        '''Test if we get the coordinates of the cities'''
        df = open_file(self.file_name)
        res = get_coordinates(df, "a")
        self.assertTrue(np.all(res == 0))

    def test_distance(self):
        '''Test distances'''
        df = open_file(self.file_name)
        distances = compute_distances(df)
        distance = get_distance(distances, "a", "b")
        self.assertEqual(1, distance)

    def test_cross_product(self):
        '''Test cross product'''
        liste = [1, 2, 3]
        cross = cross_product(liste)
        crossed = np.array([[1, 1], [1, 2], [1, 3], [2, 1],
                            [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]])
        self.assertTrue(np.array_equal(crossed, cross))

    def test_coodinates2(self):
        '''Test coordinates'''
        df = open_file(self.file_name)
        distances = compute_distances(df)
        distance = get_distance(distances, "a", "b")
        self.assertEqual(distance, 1)

    def test_compute_fitness(self):
        '''Test fitness'''
        df = open_file(self.file_name)
        distances = compute_distances(df)
        length = compute_fitness(["a", "b"], distances)
        self.assertEqual(length, 2)

    def test_greedy(self):
        '''Test greedy'''
        message = "The algorithm shouldn't return a empty list"
        res = greedy(self.file_name)
        self.assertTrue(len(res) > 0, message)

    def test_prob_to_city(self):
        '''Test prob_to_city'''
        df = open_file(self.file_name)
        distances = compute_distances(df)
        prob = prob_to_city("a", "b", ["c", "d"], distances, distances, 1, 1)
        self.assertTrue(prob is not None)


if __name__ == '__main__':
    unittest.main()
