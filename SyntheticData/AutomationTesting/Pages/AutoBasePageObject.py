import os
import csv


class AutoBasePageObject():

    def __init__(self, download_dir=None):
        self.download_dir = download_dir or os.path.expanduser("~/Downloads")

    def read_latest_csv(self):
        download_dir = self.download_dir
        csv_files = [f for f in os.listdir(download_dir) if f.endswith(".csv")]
        if not csv_files:
            raise FileNotFoundError("No CSV files found in the directory.")

        csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)    
        latest_csv = os.path.join(download_dir, csv_files[0])

        rows = []
        with open(latest_csv, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
                rows.append(row)
        assert len(rows) == 11, f"Expected 10 lines in CSV, found {len(rows)}"
        os.remove(latest_csv)
        print("CSV file has been reviewed and deleted")        
        return rows
