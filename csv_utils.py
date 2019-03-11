headings = [
    "year", "state", "state_code", "jurisdiction", "active_registration",
    "precincts", "polling_places", "poll_workers", "worker_age_group_1",
    "worker_age_group_2", "worker_age_group_3", "worker_age_group_4",
    "worker_age_group_5", "worker_age_group_6", "poll_worker_difficulty",
    "election_participants"
]

difficulty_dict = {
    "1": "Very difficult",
    "2": "Somewhat difficult",
    "3": "Neither difficult nor easy",
    "4": "Somewhat easy",
    "5": "Very easy",
    "6": "Not enough information to answer",
    "Not enough info": "Not enough information to answer",
    "Neither": "Neither difficult nor easy",
    "N/a": "Not enough information to answer"
}

workbook_data = [{
    "year": 2016,
    "sheets": [{
        "label": "SECTION A",
        "columns": [1, 2, 8]
    }, {
        "label": "SECTION D",
        "columns": [3, 5, 15, 17, 18, 19, 20, 21, 22],
        "difficulty_col": 24
    }, {
        "label": "SECTION F",
        "columns": [3]
    }]
}, {
    "year": 2014,
    "sheets": [{
        "label": "EAVS_Section_A",
        "columns": [2, 3, 9]
    }, {
        "label": "EAVS_Section_D",
        "columns": [4, 6, 17, 19, 20, 21, 22, 23, 24],
        "difficulty_col": 27
    }, {
        "label": "EAVS_Section_F",
        "columns": [4]
    }]
}, {
    "year": 2012,
    "sheets": [{
        "label": "2012NVRAData",
        "columns": [0, 1, 8]
    }, {
        "label": "Section D",
        "columns": [3, 5, 16, 18, 19, 20, 21, 22, 23],
        "difficulty_col": 26
    }, {
        "label": "Section F",
        "columns": [3]
    }]
}, {
    "year": 2010,
    "sheets": [{
        "label": "Section A",
        "columns": [0, 1, 8]
    }, {
        "label": "Section D",
        "columns": [3, 5, 16, 18, 19, 20, 21, 22, 23],
        "difficulty_col": 26
    }, {
        "label": "Section F",
        "columns": [3]
    }]
}, {
    "year": 2008,
    "sheets": [{
        "label": "SectionA",
        "columns": [3, 1, 10]
    }, {
        "label": "SectionD",
        "columns": [4, 7, 22, 25, 26, 27, 28, 29, 30],
        "difficulty_col": 33
    }, {
        "label": "SectionF",
        "columns": [4]
    }]
}]
