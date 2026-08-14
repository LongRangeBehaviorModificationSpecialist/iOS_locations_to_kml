# !/usr/bin/env python3

"""Handler configurations for all database types.

Imports query builders, header writers, row extractors, and body writers
for each database type (1-6) from their respective modules.

Usage:
    from handlers import get_handlers

    handlers = get_handlers(args.db_type)
    handlers["query"](start_time, end_time)       # Section 1
    handlers["header"]()                          # Section 2
    handlers["row"](row)                          # Section 3
    handlers["body"](row_data)                    # Section 4
"""

from typing import Callable, Dict, Any
import pandas as pd
from rich.console import Console
from rich.traceback import install

from vars.cache_sqlite import (
    cache_sqlite_query,
    cache_sqlite_kml_header,
    cache_sqlite_kml_body
)
from vars.cache_encb_wifi import (
    cache_encb_wifi_query,
    cache_encb_wifi_kml_header,
    cache_encb_wifi_kml_body
)
from vars.cache_encb_lte import(
    cache_encb_lte_query,
    cache_encb_lte_kml_header,
    cache_encb_lte_kml_body
)
from vars.cloud_v2_signif_loc import (
    cloud_v2_signif_loc_query,
    cloud_v2_signif_loc_kml_header,
    cloud_v2_signif_loc_kml_body
)
from vars.local_signif_loc_visits import (
    local_signif_loc_visits_query,
    local_signif_loc_visits_kml_header,
    local_signif_loc_visits_kml_body
)
from vars.local_vehicle_loc import (
    local_vehicle_loc_query,
    local_vehicle_loc_kml_header,
    local_vehicle_loc_kml_body
)

console=Console()
install(show_locals=True, console=console)


QUERY_BUILDERS: Dict[str, Callable[[float, float], str]] = {
    "1": lambda start_time, end_time: cache_sqlite_query(
        start_time,
        end_time,
    ),
    "2": lambda start_time, end_time: cache_encb_wifi_query(
        start_time,
        end_time,
    ),
    "3": lambda start_time, end_time: cache_encb_lte_query(
        start_time,
        end_time,
    ),
    "4": lambda start_time, end_time: cloud_v2_signif_loc_query(
        start_time,
        end_time,
    ),
    "5": lambda start_time, end_time: local_signif_loc_visits_query(
        start_time,
        end_time,
    ),
    "6": lambda start_time, end_time: local_vehicle_loc_query(
        start_time,
        end_time,
    ),
}

HEADER_WRITERS: Dict[str, Callable[[], str]] = {
    "1": cache_sqlite_kml_header,
    "2": cache_encb_wifi_kml_header,
    "3": cache_encb_lte_kml_header,
    "4": cloud_v2_signif_loc_kml_header,
    "5": local_signif_loc_visits_kml_header,
    "6": local_vehicle_loc_kml_header,
}

ROW_EXTRACTORS: Dict[str, Callable[[pd.Series], Dict[str, Any]]] = {
    "1": lambda row: {
        "record": row["record_number"],
        "Z_PK": row["z_pk"],
        "utc_time": row["timestamp_utc"],
        "local_time": row["timestamp_local"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "gps_merged": row["gps_merged"],
        "speed_meters_per_sec": row["speed_meters_sec"],
        "speed_mph": row["speed_mph"],
        "course": row["course"],
        "horiz_acc_meters": row["horiz_accuracy_meters"],
        "horiz_acc_feet": row["horiz_accuracy_feet"],
        "vert_acc_meters": row["vertical_accuracy_meters"],
        "vert_acc_feet": row["vertical_accuracy_feet"],
        "data_source": row["data_source"],
    },
    "2": lambda row: {
        "record": row["record_number"],
        "mac_address": row["mac_address"],
        "utc_time": row["timestamp_utc"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "gps_merged": row["gps_merged"],
        "channel": row["channel"],
        "horiz_accuracy": row["horizontal_accuracy"],
        "altitude": row["altitude"],
        "confidence": row["confidence"],
        "data_source": row["data_source"],
    },
    "3": lambda row: {
        "record": row["record_number"],
        "utc_time": row["timestamp_utc"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "gps_merged": row["gps_merged"],
        "mcc": row["mcc"],
        "mnc": row["mnc"],
        "tac": row["tac"],
        "ci": row["ci"],
        "horiz_accuracy": row["horizontal_accuracy"],
        "altitude": row["altitude"],
        "confidence": row["confidence"],
        "data_source": row["data_source"],
    },
    "4": lambda row: {
        "record": row["record_number"],
        "Z_PK": row["z_pk"],
        "address_info": row["address_info"],
        "probable_place_name": row["probable_place_name"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "gps_merged": row["gps_merged"],
        "uncertainty": row["uncertainty"],
        "add_create_utc": row["address_creation_date_utc"],
        "add_expire_utc": row["address_expire_date_utc"],
        "data_source": row["data_source"],
    },
    "5": lambda row: {
        "record": row["record_number"],
        "Z_PK": row["z_pk"],
        "data_point_count": row["data_point_count"],
        "location_of_interest_id": row["location_of_interest_id"],
        "creation_date_utc": row["creation_date_utc"],
        "entry_date_utc": row["entry_date_utc"],
        "exit_date_utc": row["exit_date_utc"],
        "expiration_date_utc": row["expiration_date_utc"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "gps_merged": row["gps_merged"],
        "location_horiz_uncertainty": row["location_horizontal_uncertainty"],
        "location_confidence": row["location_confidence"],
        "data_source": row["data_source"],
    },
    "6": lambda row: {
        "record": row["record_number"],
        "Z_PK": row["z_pk"],
        "utc_time": row["date_time_utc"],
        "location_time_utc": row["location_date_utc"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "gps_merged": row["gps_merged"],
        "location_uncertainty": row["location_uncertainty"],
        "identifier": row["identifier"],
        "data_source": row["data_source"],
    },
}

BODY_WRITERS: Dict[str, Callable[[Dict[str, Any]], str]] = {
    "1": lambda data: cache_sqlite_kml_body(
        record=data["record"],
        local_time=data["local_time"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        gps_merged=data["gps_merged"],
        course=data["course"],
        horiz_acc_meters=data["horiz_acc_meters"],
        utc_time=data["utc_time"],
        speed_meters_per_sec=data["speed_meters_per_sec"],
        speed_mph=data["speed_mph"],
        horiz_acc_feet=data["horiz_acc_feet"],
        vert_acc_meters=data["vert_acc_meters"],
        vert_acc_feet=data["vert_acc_feet"],
        data_source=data["data_source"],
    ),

    "2": lambda data: cache_encb_wifi_kml_body(
        record=data["record"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        gps_merged=data["gps_merged"],
        mac_address=data["mac_address"],
        channel=data["channel"],
        horiz_accuracy=data["horiz_accuracy"],
        utc_time=data["utc_time"],
        altitude=data["altitude"],
        confidence=data["confidence"],
        data_source=data["data_source"],
    ),

    "3": lambda data: cache_encb_lte_kml_body(
        record=data["record"],
        utc_time=data["utc_time"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        gps_merged=data["gps_merged"],
        site_info=(
            f"mcc: {data['mcc']} | mnc: {data['mnc']} | tac: {data['tac']} "
            f"| ci: {data['ci']}"
        ),
        horiz_accuracy=data["horiz_accuracy"],
        altitude=data["altitude"],
        confidence=data["confidence"],
        data_source=data["data_source"],
    ),

    "4": lambda data: cloud_v2_signif_loc_kml_body(
        record=data["record"],
        Z_PK=data["Z_PK"],
        address_info=data["address_info"],
        probable_place_name=data["probable_place_name"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        gps_merged=data["gps_merged"],
        uncertainty=data["uncertainty"],
        add_create_utc=data["add_create_utc"],
        add_expire_utc=data["add_expire_utc"],
        data_source=data["data_source"],
    ),

    "5": lambda data: local_signif_loc_visits_kml_body(
        record=data["record"],
        data_point_count=data["data_point_count"],
        location_of_interest_id=data["location_of_interest_id"],
        creation_date_utc=data["creation_date_utc"],
        entry_date_utc=data["entry_date_utc"],
        exit_date_utc=data["exit_date_utc"],
        expiration_date_utc=data["expiration_date_utc"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        gps_merged=data["gps_merged"],
        location_horiz_uncertainty=data["location_horiz_uncertainty"],
        location_confidence=data["location_confidence"],
        data_source=data["data_source"],
    ),

    "6": lambda data: local_vehicle_loc_kml_body(
        record=data["record"],
        utc_time=data["utc_time"],
        location_time_utc=data["location_time_utc"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        gps_merged=data["gps_merged"],
        location_uncertainty=data["location_uncertainty"],
        identifier=data["identifier"],
        data_source=data["data_source"]
    ),
}

VALID_DB_TYPES = ("1", "2", "3", "4", "5", "6")

def get_handlers(db_type: str) -> Dict[str, Callable]:
    """Get all handlers for a given db_type.

    Args:
        db_type: Database type identifier ("1" through "6")

    Returns:
        Dictionary with keys: "query", "header", "row", "body"

    Raises:
        KeyError: If db_type is not supported
    """
    if db_type not in VALID_DB_TYPES:
        raise KeyError(
            f"Unsupported database type: '{db_type}'. "
            f"Must be one of: {', '.join(VALID_DB_TYPES)}"
        )

    return {
        "query": QUERY_BUILDERS[db_type],
        "header": HEADER_WRITERS[db_type],
        "row": ROW_EXTRACTORS[db_type],
        "body": BODY_WRITERS[db_type],
    }


def validate_all_handlers_exist() -> None:
    """Validate that all handlers are properly registered.

    Call this once at startup during development to catch missing
    registrations early (e.g., forgot to add db_type "7").

    Raises:
        AssertionError: If any db_type is missing handlers
    """
    for db_type in VALID_DB_TYPES:
        assert db_type in QUERY_BUILDERS, f"Missing query builder for db_type {db_type}"
        assert db_type in HEADER_WRITERS, f"Missing header writer for db_type {db_type}"
        assert db_type in ROW_EXTRACTORS, f"Missing row extractor for db_type {db_type}"
        assert db_type in BODY_WRITERS, f"Missing body writer for db_type {db_type}"
