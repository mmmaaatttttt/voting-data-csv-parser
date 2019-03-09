from utils import clear_file, record_data
from csv_utils import workbook_data


csv_file_name = "voting_data.csv"


clear_file(csv_file_name)
for d in workbook_data:
    record_data(**d, write_path=csv_file_name)
