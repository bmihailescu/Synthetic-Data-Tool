import unittest
import sys
import os
import contextlib
import io
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website.SyntheticApp import generate_data

class TestCaseNumberBoundaryValues(unittest.TestCase):

    #Test case that will test generated Number boundaries between 1 and 1001

    def test_generate_1_number(self):

        num_of_entries = 1
        column_name_array = ["Number Column"]
        data_type_array = ["Number"]
        format_list = ["1, 100"]
        blank_perc_list = [0]
        bad_data_list = [0]
        file_type = 'csv'


        with contextlib.redirect_stdout(io.StringIO()):
            gen = generate_data(num_of_entries,
                column_name_array, 
                data_type_array, 
                format_list, 
                blank_perc_list, 
                bad_data_list,file_type)

        file_path = "SyntheticData.csv"

        with open("SyntheticData.csv", "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            print("Test Completed for 1 entries")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")          

    def test_generate_999_numbers(self):

        num_of_entries = 999
        column_name_array = ["Number Column"]
        data_type_array = ["Number"]
        format_list = ["1, 100"]
        blank_perc_list = [0]
        bad_data_list = [0]
        file_type = 'csv'

        with contextlib.redirect_stdout(io.StringIO()):
            gen = generate_data(num_of_entries,
                column_name_array, 
                data_type_array, 
                format_list, 
                blank_perc_list, 
                bad_data_list,file_type)

        file_path = "SyntheticData.csv"

        with open("SyntheticData.csv", "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1000)
            print("Test Completed for 999 entries")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      


    def test_generate_1000_numbers(self):

        num_of_entries = 1000
        column_name_array = ["Number Column"]
        data_type_array = ["Number"]
        format_list = ["1, 100"]
        blank_perc_list = [0]
        bad_data_list = [0]
        file_type = 'csv'

        with contextlib.redirect_stdout(io.StringIO()):
            gen = generate_data(num_of_entries,
                column_name_array, 
                data_type_array, 
                format_list, 
                blank_perc_list, 
                bad_data_list,file_type)

        file_path = "SyntheticData.csv"

        with open("SyntheticData.csv", "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1001)
            print("Test Completed for 1000 entries")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      


    def test_generate_1001_numbers(self):

        num_of_entries = 1001
        column_name_array = ["Number Column"]
        data_type_array = ["Number"]
        format_list = ["1, 100"]
        blank_perc_list = [0]
        bad_data_list = [0]
        file_type = 'csv'

        with contextlib.redirect_stdout(io.StringIO()):
            gen = generate_data(num_of_entries,
                column_name_array, 
                data_type_array, 
                format_list, 
                blank_perc_list, 
                bad_data_list,file_type)

        file_path = "SyntheticData.csv"

        with open("SyntheticData.csv", "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1002)
            print("Test Completed for 1001 entries")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")                                                                          


if __name__ == '__main__':
    unittest.main()