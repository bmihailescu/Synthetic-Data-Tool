import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website.SyntheticApp import generate_data
from TestingBasePageObject import TestingBasePageObject

class TestCaseDataTypeName(unittest.TestCase):

    #Test case that will generate Names at random


    #Test funtion that will generate 10 Full Names at random
    def test_generate_10_full_names(self):

        num_of_entries = 10
        column_name_array = ["Full Name Column"]
        data_type_array = ["Name"]
        format_list = ["fullName"]
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



    #Test funtion that will generate 10 First Names at random

    def test_generate_10_first_names(self):

        num_of_entries = 10
        column_name_array = ["First Name Column"]
        data_type_array = ["Name"]
        format_list = ["firstName"]
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



    #Test funtion that will generate 10 Last Names at random
    
    def test_generate_10_last_names(self):

        num_of_entries = 10
        column_name_array = ["Last Name Column"]
        data_type_array = ["Name"]
        format_list = ["lastName"]
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