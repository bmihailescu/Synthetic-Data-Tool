import unittest
import sys
import os
import contextlib
import io
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website.SyntheticApp import generate_data

class TestCaseDataTypeName(unittest.TestCase):

    #Test case that will generate Names at random

    #Full Names
    def test_generate_1_full_names(self):

        num_of_entries = 1
        column_name_array = ["Full Name Column"]
        data_type_array = ["Name"]
        format_list = ["fullName"]
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
            print("Test Completed for 0 entries for Full Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1_full_name(self):

        num_of_entries = 1
        column_name_array = ["Full Name Column"]
        data_type_array = ["Name"]
        format_list = ["fullName"]
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
            print("Test Completed for 1 entries for Full Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_999_full_names(self):

        num_of_entries = 999
        column_name_array = ["Full Name Column"]
        data_type_array = ["Name"]
        format_list = ["fullName"]
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
            print("Test Completed for 999 entries for Full Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1000_full_names(self):

        num_of_entries = 1000
        column_name_array = ["Full Name Column"]
        data_type_array = ["Name"]
        format_list = ["fullName"]
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
            print("Test Completed for 1000 entries for Full Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1001_full_names(self):

        num_of_entries = 1001
        column_name_array = ["Full Name Column"]
        data_type_array = ["Name"]
        format_list = ["fullName"]
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
            print("Test Completed for 1001 entries for Full Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")                                


    #First Names
    def test_generate_0_first_names(self):

        num_of_entries = 1
        column_name_array = ["First Name Column"]
        data_type_array = ["Name"]
        format_list = ["firstName"]
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
            print("Test Completed for 0 entries for First Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1_first_name(self):

        num_of_entries = 1
        column_name_array = ["First Name Column"]
        data_type_array = ["Name"]
        format_list = ["firstName"]
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
            print("Test Completed for 1 entries for First Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_999_first_names(self):

        num_of_entries = 999
        column_name_array = ["First Name Column"]
        data_type_array = ["Name"]
        format_list = ["firstName"]
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
            print("Test Completed for 999 entries for First Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1000_first_names(self):

        num_of_entries = 1000
        column_name_array = ["First Name Column"]
        data_type_array = ["Name"]
        format_list = ["firstName"]
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
            print("Test Completed for 1000 entries for First Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1001_first_names(self):

        num_of_entries = 1001
        column_name_array = ["First Name Column"]
        data_type_array = ["Name"]
        format_list = ["firstName"]
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
            print("Test Completed for 1001 entries for First Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")              

    #Last Names
    def test_generate_0_last_names(self):

        num_of_entries = 1
        column_name_array = ["Last Name Column"]
        data_type_array = ["Name"]
        format_list = ["lastName"]
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
            print("Test Completed for 0 entries for Last Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1_last_name(self):

        num_of_entries = 1
        column_name_array = ["Last Name Column"]
        data_type_array = ["Name"]
        format_list = ["lastName"]
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
            print("Test Completed for 1 entries for Last Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")  

    def test_generate_999_last_names(self):

        num_of_entries = 999
        column_name_array = ["Last Name Column"]
        data_type_array = ["Name"]
        format_list = ["lastName"]
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
            print("Test Completed for 999 entries for Last Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1000_last_names(self):

        num_of_entries = 1000
        column_name_array = ["Last Name Column"]
        data_type_array = ["Name"]
        format_list = ["lastName"]
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
            print("Test Completed for 1000 entries for Last Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")      

    def test_generate_1001_last_names(self):

        num_of_entries = 1001
        column_name_array = ["Last Name Column"]
        data_type_array = ["Name"]
        format_list = ["lastName"]
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
            print("Test Completed for 1001 entries for Last Name")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")                       
        
if __name__ == '__main__':
    unittest.main()