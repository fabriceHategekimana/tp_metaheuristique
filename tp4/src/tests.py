import unittest
import numpy as np
from module import (open_file, get_coordinates,
                    cross_product, compute_distances,
                    get_distance, compute_fitness)


class AS_test(unittest.TestCase):

    # be sure to use the prefix "test_"
    def test_coodinates(self):
        '''Test if we get the coordinates of the cities'''
        df = open_file("cities.dat")
        res = get_coordinates(df, "a")
        self.assertEqual((0, 0), res)

    def test_distance(self):
        '''Test distances'''
        df = open_file("cities.dat")
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
        df = open_file("cities.dat")
        distances = compute_distances(df)
        distance = get_distance(distances, "a", "b")
        self.assertEqual(distance, 1)
        # self.assertTrue(True)

    def test_compute_fitness(self):
        '''Test fitness'''
        df = open_file("cities.dat")
        distances = compute_distances(df)
        length = compute_fitness(["a", "b"], distances)
        self.assertEqual(length, 2)


if __name__ == '__main__':
    unittest.main()
