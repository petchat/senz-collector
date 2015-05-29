# -*- coding: utf-8 -*-

__author__ = 'jiaying.lu'

from unittest import TestCase
import numpy as np

from flask_app.timesequence_align import _get_sequence_length, _get_time_distribution_params, _get_time_distribution


class TestBaseMethod(TestCase):

    def test_get_sequence_length(self):
        tmp_list = range(10)
        self.assertEqual(10, _get_sequence_length(tmp_list))


    def test_get_time_distribution_params(self):
        # case 1
        sequence_list = np.array([[1, 3, 6],
                                  [3, 4, 7, 9],
                                  [2, 4, 6, 9]]) 
        self.assertEqual((2, 2), _get_time_distribution_params(sequence_list))

        # case 2
        sequence_list = np.array([[1],
                                  [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23],
                                  [2, 4, 6, 9]]) 
        self.assertEqual((3, 6), _get_time_distribution_params(sequence_list))


    def test_get_time_distribution(self):
        # case 1
        sequence = np.array([1, 2])
        self.assertEqual(0, _get_time_distribution(sequence, 1, 2))
        # case 2
        sequence = np.array([1, 2, 3, 4])
        self.assertEqual(0, _get_time_distribution(sequence, 1, 2))

        # case 3
        sequence = np.array([1, 3, 5])
        self.assertEqual(1, _get_time_distribution(sequence, 1, 2))

        # case 4
        sequence = np.array([1, 2, 3, 4, 5, 6])
        self.assertEqual(8, _get_time_distribution(sequence, 1, 2))
        # case 5
        sequence = np.array([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(8, _get_time_distribution(sequence, 1, 2))

    
    def test_generate_sequences_measures(self):
        pass
