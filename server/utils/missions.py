MISSIONS = {
    "XMM": {
        "table": "xmmmaster",
        "id_column": "obsid",
        "exposure_column": "duration",
        "extra_columns": [],
    },
    "Chandra": {
        "table": "chanmaster",
        "id_column": "obsid",
        "exposure_column": "exposure",
        "extra_columns": [],
    },
    "NuSTAR": {
        "table": "numaster",
        "id_column": "obsid",
        "exposure_column": "exposure_a",
        "extra_columns": [],
    },
    "NICER": {
        "table": "nicermastr",
        "id_column": "obsid",
        "exposure_column": "exposure",
        "extra_columns": ["obs_type", "processing_status"],
    },
}

SUPPORTED_MISSIONS = list(MISSIONS.keys())
