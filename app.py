from xlrd import open_workbook
from csv import writer
from decorators import log_start_and_end
from headings import headings
from paths import paths
from states import states, states_by_abbreviation
import sys

csv_file_name = "voting_data.csv"


def clear_file(path):
    with open(path, "w") as csvfile:
        data_writer = writer(csvfile)
        data_writer.writerow(headings)


def clean(record):
    invalid_records = [
        '-999999: Data Not Available', '-888888: Not Applicable', '-9999999',
        '-8888888', '-6666666', '-88888', -999999, '-',
        'Not enough information to answer'
    ]
    return None if record in invalid_records else record


@log_start_and_end
def record_data_2016(write_path):
    year = 2016
    data_by_state_and_juris = {}
    wb = open_workbook(paths[year])
    a_sheet = wb.sheet_by_name("SECTION A")
    d_sheet = wb.sheet_by_name("SECTION D")
    f_sheet = wb.sheet_by_name("SECTION F")

    for ridx in range(1, a_sheet.nrows):
        a_rows = a_sheet.row_values(ridx)
        a_indices = [1, 2, 8]
        [state_code, jurisdiction,
         registrations] = [a_rows[idx] for idx in a_indices]
        state = states_by_abbreviation.get(state_code)
        if state:
            key = f"{state_code}|{jurisdiction}"
            data_by_state_and_juris[key] = [
                year, state, state_code,
                jurisdiction.title(),
                clean(registrations)
            ]

    for ridx in range(1, d_sheet.nrows):
        d_rows = d_sheet.row_values(ridx)
        d_indices = [3, 5, 15, 17, 18, 19, 20, 21, 22, 24]
        key = f"{d_rows[1]}|{d_rows[2]}"
        data_list = data_by_state_and_juris.get(key)
        if data_list:
            data_list.extend(clean(d_rows[idx]) for idx in d_indices)

    for ridx in range(1, f_sheet.nrows):
        f_rows = f_sheet.row_values(ridx)
        f_indices = [3]
        key = f"{f_rows[1]}|{f_rows[2]}"
        data_list = data_by_state_and_juris.get(key)
        if data_list:
            data_list.extend(clean(f_rows[idx]) for idx in f_indices)

    with open(write_path, "a") as csvfile:
        data_writer = writer(csvfile)
        for key in data_by_state_and_juris:
            data_writer.writerow(data_by_state_and_juris[key])


@log_start_and_end
def record_data_2014(write_path):
    year = 2014
    data_by_state_and_juris = {}
    wb = open_workbook(paths[year])
    a_sheet = wb.sheet_by_name("EAVS_Section_A")
    d_sheet = wb.sheet_by_name("EAVS_Section_D")
    f_sheet = wb.sheet_by_name("EAVS_Section_F")

    for ridx in range(1, a_sheet.nrows):
        a_rows = a_sheet.row_values(ridx)
        a_indices = [2, 3, 9]
        [state_code, jurisdiction,
         registrations] = [a_rows[idx] for idx in a_indices]
        state = states_by_abbreviation.get(state_code)
        if state:
            key = f"{state_code}|{jurisdiction}"
            data_by_state_and_juris[key] = [
                year, state, state_code,
                jurisdiction.title(),
                clean(registrations)
            ]

    for ridx in range(1, d_sheet.nrows):
        d_rows = d_sheet.row_values(ridx)
        d_indices = [4, 6, 17, 19, 20, 21, 22, 23, 24, 27]
        key = f"{d_rows[2]}|{d_rows[3]}"
        data_list = data_by_state_and_juris.get(key)
        if data_list:
            data_list.extend(clean(d_rows[idx]) for idx in d_indices)

    for ridx in range(1, f_sheet.nrows):
        f_rows = f_sheet.row_values(ridx)
        f_indices = [4]
        key = f"{f_rows[2]}|{f_rows[3]}"
        data_list = data_by_state_and_juris.get(key)
        if data_list:
            data_list.extend(clean(f_rows[idx]) for idx in f_indices)

    with open(write_path, "a") as csvfile:
        data_writer = writer(csvfile)
        for key in data_by_state_and_juris:
            data_writer.writerow(data_by_state_and_juris[key])


clear_file("voting_data_2014-2016.csv")
record_data_2016("voting_data_2014-2016.csv")
record_data_2014("voting_data_2014-2016.csv")

# def record_data_2012(directory, write_path):
# year - 2012
# state - states_by_abbreviation[2012NVRAData.State]
# state_code - 2012NVRAData.State ( A / 0 )
# jurisdiction - 2012NVRAData.Jurisdiction ( B / 1 )
# precints - Section D.QD1a (D / 3)
# polling_places - Section D.QD2a (F / 5)
# poll_workers - Section D.QD3a (Q / 16)
# active registration - 2012NVRAData.QA3a (I / 8)
# election_participants - Section F.QF1a (D / 3)

# age distribution of poll workers?? (D4a-D4f)
# difficulty in finding poll workers?? (D5)

# def record_data_2010(directory):
# year - 2010
# state - states_by_abbreviation[Section A.State]
# state_code - Section A.State ( A / 0 )
# jurisdiction - Section A.Jurisdiction ( B / 1 )
# precints - Section D.QD1a (D / 3)
# polling_places - Section D.QD2a (F / 5)
# poll_workers - Section D.QD3a (Q / 16)
# active registration - Section A.QA3a (I / 8)
# election_participants - Section F.QF1a (D / 3)

# age distribution of poll workers?? (D4a-D4f)
# difficulty in finding poll workers?? (D5)

# def record_data_2008(directory):
# year - 2010
# state - SectionA.STATE_NAME ( C / 2 )
# state_code - SectionA.STATE_ ( D / 3 )
# jurisdiction - SectionA.JurisName ( B / 1 )
# precints - SectionD.D1 (E / 4)
# polling_places - SectionD.D2a (H / 7)
# poll_workers - SectionD.D3 (W / 22)
# active registration - SectionA.A3a (K / 10)
# election_participants - SectionF.F1a (E / 4)

# age distribution of poll workers?? (D4a-D4f)
# difficulty in finding poll workers?? (D5)

# def record_data_2004(directory, path):
#     start_idx = 6
#     for state in states.keys():
#         state_abbrev = states[state]
#         wb = open_workbook(f"{directory}/{state}_Jurisdictions.xls")
#         population_sheet = wb.sheet_by_name('Population Estimates')
#         poll_worker_sheet = wb.sheet_by_name('Poll Workers')  # cols 4, 5, 6
#         ballots_sheet = wb.sheet_by_name('Ballots Counted')  # cols 4, 5, 6, 7
#         absentee_sheet = wb.sheet_by_name('Absentee')  # cols 5, 7, 9
#         provisional_sheet = wb.sheet_by_name('Provisional')  # cols 6, 9
#         jurisdictions = [
#             j.value
#             for j in population_sheet.col_slice(colx=3, start_rowx=start_idx)
#         ][:-4]
#         with open(path, "a") as csvfile:
#             data_writer = writer(csvfile)
#             for idx, juris in enumerate(jurisdictions):
#                 cell_row = start_idx + idx
#                 data_writer.writerow([
#                     2004, state, state_abbrev, juris,
#                     poll_worker_sheet.cell(cell_row, 4).value,
#                     poll_worker_sheet.cell(cell_row, 5).value,
#                     poll_worker_sheet.cell(cell_row, 6).value,
#                     ballots_sheet.cell(cell_row, 4).value,
#                     ballots_sheet.cell(cell_row, 5).value,
#                     ballots_sheet.cell(cell_row, 6).value,
#                     ballots_sheet.cell(cell_row, 7).value,
#                     absentee_sheet.cell(cell_row, 5).value,
#                     absentee_sheet.cell(cell_row, 7).value,
#                     absentee_sheet.cell(cell_row, 9).value,
#                     provisional_sheet.cell(cell_row, 6).value,
#                     provisional_sheet.cell(cell_row, 9).value
#                 ])
#         print(f"{state} data recorded.")

# def record_data_2006(read_file_path, write_file_path):
#     rows_dict = {}
#     wb = open_workbook(read_file_path)

# in this sheet
# year - 2006
# state - juri_02_34.state (B / 1)
# state_code - states[state]
# jurisdiction - juri_02_34.county (C / 2)
# precints - juri_set3c.q50 (DI / 112)
# polling_places - juri_set3c.q51 (DL / 115)
# poll_workers - juri_set3c.q46 (DC / 106)
# voting_age_pop
# citizen_voting_age_pop
# registration - juri_02_34.q022006total (N / 13)
# ballots_counted - juri_set3a.q34total (AP / 41)
# absentee_requested - Sheet1.q38total (I / 8)
# absentee_returned - Sheet1.q39total (S / 18)
# absentee_counted -
# provisional_cast - juri_set3a.q33p (T / 19)
# provisional_counted  - juri_set3a.q34p (AN / 39)

#     first_sheet = wb.sheet_by_name("juri_02_34")

# for state in state.keys():
# state_abbrev = states[state]

# year -
# state -
# state_code -
# jurisdiction -
# precints -
# polling_places -
# poll_workers -
# voting_age_pop -
# citizen_voting_age_pop -
# registration -
# ballots_counted -
# absentee_requested -
# absentee_returned -
# absentee_counted -
# provisional_cast -
# provisional_counted -
