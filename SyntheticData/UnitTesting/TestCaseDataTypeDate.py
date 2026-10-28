import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website.SyntheticApp import generate_data
from TestingBasePageObject import TestingBasePageObject
class TestCaseDataTypeDate(unittest.TestCase):

    #Test case that will generate 10 Dates at ramdom

    def test_generate_10_dates(self):

        num_of_entries = 10
        column_name_array = ["Date Column"]
        data_type_array = ["Date"]
        format_list = ["%d/%m/%y,1900-01-01,2000-01-01"]
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