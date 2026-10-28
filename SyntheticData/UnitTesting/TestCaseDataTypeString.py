import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website.SyntheticApp import generate_data
from TestingBasePageObject import TestingBasePageObject

class TestCaseDataTypeString(unittest.TestCase):
        
    #Test case that will generate 10 strings with a length of 5 characters

    def test_generate_10_Strings(self):

        num_of_entries = 10
        column_name_array = ["String Column"]
        data_type_array = ["String"]
        format_list = ["5"]
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