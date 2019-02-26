from xlrd import open_workbook
from csv import writer
from headings import headings
from states import states
import sys

csv_file_name = "voting_data.csv"


def clear_file(path):
    with open(path, "w") as csvfile:
        data_writer = writer(csvfile)
        data_writer.writerow(headings)


def record_data_2004(directory, path):
    start_idx = 6
    for state in states.keys():
        state_abbrev = states[state]
        wb = open_workbook(f"{directory}/{state}_Jurisdictions.xls")
        population_sheet = wb.sheet_by_name('Population Estimates')
        poll_worker_sheet = wb.sheet_by_name('Poll Workers')  # cols 4, 5, 6
        ballots_sheet = wb.sheet_by_name('Ballots Counted')  # cols 4, 5, 6, 7
        absentee_sheet = wb.sheet_by_name('Absentee')  # cols 5, 7, 9
        provisional_sheet = wb.sheet_by_name('Provisional')  # cols 6, 9
        jurisdictions = [
            j.value
            for j in population_sheet.col_slice(colx=3, start_rowx=start_idx)
        ][:-4]
        with open(path, "a") as csvfile:
            data_writer = writer(csvfile)
            for idx, juris in enumerate(jurisdictions):
                cell_row = start_idx + idx
                data_writer.writerow([
                    2004, state, state_abbrev, juris,
                    poll_worker_sheet.cell(cell_row, 4).value,
                    poll_worker_sheet.cell(cell_row, 5).value,
                    poll_worker_sheet.cell(cell_row, 6).value,
                    ballots_sheet.cell(cell_row, 4).value,
                    ballots_sheet.cell(cell_row, 5).value,
                    ballots_sheet.cell(cell_row, 6).value,
                    ballots_sheet.cell(cell_row, 7).value,
                    absentee_sheet.cell(cell_row, 5).value,
                    absentee_sheet.cell(cell_row, 7).value,
                    absentee_sheet.cell(cell_row, 9).value,
                    provisional_sheet.cell(cell_row, 6).value,
                    provisional_sheet.cell(cell_row, 9).value
                ])
        print(f"{state} data recorded.")


clear_file(csv_file_name)
record_data_2004(sys.argv[1], csv_file_name)
