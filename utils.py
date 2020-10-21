from xlrd import open_workbook
from csv import writer, DictReader, DictWriter
from decorators import log_start_and_end
from csv_utils import headings, difficulty_dict
from paths import paths
from states import states, voting_age_estimates
from stringcase import snakecase


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


def get_or_0(dictionary, key):
    return dictionary.get(key) or 0


def aggregate_data(read_path, write_path):
    initial_dict = {
        "num_jurisdictions": 0,
        "active_registration": 0,
        "election_participants": 0,
        "eligible_voters_estimated": 0,
        "jurisdictions_with_precinct_info": 0,
        "jurisdictions_with_polling_place_info": 0,
        "jurisdictions_with_poll_worker_count": 0,
        "jurisdictions_with_age_info": 0,
        "jurisdictions_with_difficulty_info": 0,
        "registrants_in_jurisdictions_with_precinct_info": 0,
        "registrants_in_jurisdictions_with_polling_place_info": 0,
        "registrants_in_jurisdictions_with_poll_worker_info": 0,
        "registrants_in_jurisdictions_with_poll_worker_age_info": 0,
        "registrants_in_jurisdictions_with_difficulty_info": 0,
        "participants_in_jurisdictions_with_precinct_info": 0,
        "participants_in_jurisdictions_with_polling_place_info": 0,
        "participants_in_jurisdictions_with_poll_worker_info": 0,
        "participants_in_jurisdictions_with_poll_worker_age_info": 0,
        "participants_in_jurisdictions_with_difficulty_info": 0,
        "precincts": 0,
        "polling_places": 0,
        "poll_workers": 0,
        "worker_age_group_1": 0,
        "worker_age_group_2": 0,
        "worker_age_group_3": 0,
        "worker_age_group_4": 0,
        "worker_age_group_5": 0,
        "worker_age_group_6": 0
    }
    difficulties = set(val for val in difficulty_dict.values())
    for difficulty in difficulties:
        initial_dict[f"difficulty_{snakecase(difficulty)}"] = 0
    data_by_state_and_year = {}
    with open(read_path) as readfile:
        reader = DictReader(readfile)
        for row in reader:
            year = row['year']
            state = row['state']
            data_by_state_and_year[year] = data_by_state_and_year.get(year, {})
            data_by_year = data_by_state_and_year[year]
            data_by_year[state] = data_by_year.get(state, initial_dict.copy())
            d = data_by_year[state]
            d["eligible_voters_estimated"] = voting_age_estimates[int(year)][state]
            d["num_jurisdictions"] += 1
            registrants = float(get_or_0(row, "active_registration"))
            participants = float(get_or_0(row, "election_participants"))
            d["active_registration"] += registrants
            d["election_participants"] += participants
            if row.get("precincts"):
                d["jurisdictions_with_precinct_info"] += 1
                d["registrants_in_jurisdictions_with_precinct_info"] += registrants
                d["participants_in_jurisdictions_with_precinct_info"] += participants
                d["precincts"] += float(get_or_0(row, "precincts"))
            if row.get("polling_places"):
                d["jurisdictions_with_polling_place_info"] += 1
                d["registrants_in_jurisdictions_with_polling_place_info"] += registrants
                d["participants_in_jurisdictions_with_polling_place_info"] += participants
                d["polling_places"] += float(get_or_0(row, "polling_places"))
            if row.get("poll_workers"):
                d["jurisdictions_with_poll_worker_count"] += 1
                d["registrants_in_jurisdictions_with_poll_worker_info"] += registrants
                d["participants_in_jurisdictions_with_poll_worker_info"] += participants
                d["poll_workers"] += float(get_or_0(row, "poll_workers"))
            if row.get("worker_age_group_1"):
                d["jurisdictions_with_age_info"] += 1
                d["registrants_in_jurisdictions_with_poll_worker_age_info"] += registrants
                d["participants_in_jurisdictions_with_poll_worker_age_info"] += participants
                d["worker_age_group_1"] += float(get_or_0(row, "worker_age_group_1"))
                d["worker_age_group_2"] += float(get_or_0(row, "worker_age_group_2"))
                d["worker_age_group_3"] += float(get_or_0(row, "worker_age_group_3"))
                d["worker_age_group_4"] += float(get_or_0(row, "worker_age_group_4"))
                d["worker_age_group_5"] += float(get_or_0(row, "worker_age_group_5"))
                d["worker_age_group_6"] += float(get_or_0(row, "worker_age_group_6"))
            if row.get("poll_worker_difficulty"):
                d["jurisdictions_with_difficulty_info"] += 1
                d["registrants_in_jurisdictions_with_difficulty_info"] += registrants
                d["participants_in_jurisdictions_with_difficulty_info"] += participants
                d[f"difficulty_{snakecase(row['poll_worker_difficulty'])}"] += 1

    with open(write_path, "w") as writefile:
        fieldnames = ["year", "state", *initial_dict.keys()]
        writer = DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for year in data_by_state_and_year:
            for state in data_by_state_and_year[year]:
                writer.writerow({
                    "year": year,
                    "state": state,
                    **data_by_state_and_year[year][state]
                })