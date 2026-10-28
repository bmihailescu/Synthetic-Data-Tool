import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website.SyntheticApp import generate_data
from TestingBasePageObject import TestingBasePageObject

class TestCaseDataTypeMC(unittest.TestCase):

    #Test case that will generate 10 Multiple Choice from 3 criteria

    def test_generate_10_multiple_choice(self):

        num_of_entries = 10
        column_name_array = ["Multiple Choice Column"]
        data_type_array = ["Multiple_Choice"]
        format_list = ["Red, Green, Blue"]
        blank_perc_list = [0]
        bad_data_list = [0]
        file_type = 'csv'

        gen = generate_data(num_of_entries,
            column_name_array, 
            data_type_array, 
            format_list, 
            blank_perc_list, 
            bad_data_list,
            file_type)

        TestingBasePageObject.openAndCheckFile(self)


if __name__ == '__main__':
    unittest.main()