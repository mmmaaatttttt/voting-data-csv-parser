from xlrd import open_workbook
from csv import writer
from decorators import log_start_and_end
from csv_utils import headings, difficulty_dict
from paths import paths
from states import states


def clear_file(path):
    with open(path, "w") as csvfile:
        data_writer = writer(csvfile)
        data_writer.writerow(headings)


def clean(record):
    invalid_records = [
        '-999999: Data Not Available', '-888888: Not Applicable', '-9999999',
        '-8888888', '-6666666', '-88888', -999999, '-',
        '-888888: not applicable', '-999999: data not available'
    ]
    return None if record in invalid_records else record


def clean_difficulty(difficulty_str):
    formatted_str = difficulty_str.capitalize().strip()
    if len(formatted_str) > 0:
        first_char = formatted_str[0]
        if difficulty_dict.get(first_char):
            return difficulty_dict.get(first_char)
    if difficulty_dict.get(formatted_str):
        return difficulty_dict.get(formatted_str)
    return formatted_str


@log_start_and_end
def record_data(year, sheets, write_path):
    data_by_state_and_juris = {}
    wb = open_workbook(paths[year])

    first_sheet = wb.sheet_by_name(sheets[0]["label"])

    for ridx in range(1, first_sheet.nrows):
        first_sheet_cols = first_sheet.row_values(ridx)
        [state_code, jurisdiction, registrations] = [
            first_sheet_cols[idx] for idx in sheets[0]["columns"]
        ]
        state = states.get(state_code)
        if state:
            key = f"{state_code}|{jurisdiction}"
            data_by_state_and_juris[key] = [
                year, state, state_code,
                jurisdiction.title(),
                clean(registrations)
            ]

    for sheet_data in sheets[1:]:
        sheet = wb.sheet_by_name(sheet_data["label"])
        for ridx in range(1, sheet.nrows):
            cols = sheet.row_values(ridx)
            key_cols = sheets[0]["columns"][:2]
            key = f"{cols[key_cols[0]]}|{cols[key_cols[1]]}"
            data_list = data_by_state_and_juris.get(key)
            if data_list:
                data_list.extend(
                    clean(cols[idx]) for idx in sheet_data["columns"])
                if sheet_data.get("difficulty_col"):
                    idx = sheet_data["difficulty_col"]
                    data_list.append(clean(clean_difficulty(cols[idx])))

    with open(write_path, "a") as csvfile:
        data_writer = writer(csvfile)
        for key in data_by_state_and_juris:
            data_writer.writerow(data_by_state_and_juris[key])
