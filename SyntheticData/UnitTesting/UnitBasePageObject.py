import os

class UnitBasePageObject():
     
     @staticmethod
     def openAndCheckFile(self):
       
        file_path = "SyntheticData.csv"
         
        with open("SyntheticData.csv", "r") as f:
            lines = f.readlines()
            for line in lines:
                print(line.strip())
            self.assertEqual(len(lines), 11)
            
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path + " has been deleted")   