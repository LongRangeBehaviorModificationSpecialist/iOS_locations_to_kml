# !/usr/bin/env python3

import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from rich.console import Console
from rich.traceback import install
from rich.panel import Panel

from shared.timezones import US_TIME_ZONES
from functions.get_options import GetOptions
from utils import Utils


__author__ = "@mikes"
__dlu__ = "11-Jun-2026"
__version__ = "1.2.1"


# Create the console object
console = Console()
install(show_locals=True, console=console)


def print_help() -> None:
    # A standard docstring-style help menu
    help_text = f"""
Usage: python .\make_kml_prompted.py ["-h", "--help"]

An interactive tool to process location database caches.

Options:
    -h, --help    Show this help message and exit.

Author:
    {__author__}

Version:
    {__version__}

Last Updated:
    {__dlu__}

Arguments:
    None

Database Options:
    1 = Cache.sqlite (Location History)
    2 = cache_encryptedB.db (WiFi locations)
    3 = cache_encryptedB.db (LTE locations)
    4 = Cloud-V2.sqlite (Significant Locations)
    5 = Local.sqlite (Significant Location Visits) or
    6 = Local.sqlite (Vehicle Locations)

Date/Time Entries:
    Must be entered using the following format: "YYYY-MM-DD HHMMSS"
    Do not use quotes around the input values

Timezone Option:
    Valid options are:
        ["ET","EST","EDT"] = "America/New_York",
        ["CT","CST","CDT"] = "America/Chicago",
        ["MT","MST","MDT"] = "America/Denver",
        ["AZ"]             = "America/Phoenix" (no DST),
        ["PT","PST","PDT"] = "America/Los_Angeles",
        ["AKT"]            = "America/Anchorage",
        ["HT","HST"]       = "Pacific/Honolulu",
        ["UTC","GMT"]      = UTC timezone
"""
    console.print(f"[yellow]{help_text}")
    # Exit cleanly
    sys.exit(0)


def get_options():
    """Get the required options to pass to the make_kml() function."""
    # Display a script header panel
    console.print("")
    console.print(
        Panel.fit(
            "[bold][cyan]Make .kml from database file[/bold][grey66]\n"
            "[dim]Please answer the following questions to configure the "
            "application.[/dim]",
            border_style="cyan"
        )
    )

    # Ask questions to get the variables for the make_kml_prompted() function
    # Using rich to display the final arguments
    source     = GetOptions.get_source_path()
    dest       = GetOptions.get_dest_path()
    destf      = GetOptions.get_destf_name()
    csv        = GetOptions.get_csv_option()
    db         = GetOptions.get_db_option()
    start_time = GetOptions.get_start_time()
    end_time   = GetOptions.get_end_time()
    tz         = GetOptions.get_tz_options()

    make_kml(
        source=source,
        dest=dest,
        # destf=destf,
        make_csv=make_csv,
        db_type=db_type,
        start_time=start_time,
        end_time=end_time,
        tz_code=tz_code
    )


def make_kml(
        source: Path,
        dest: Path,
        # destf: str,
        make_csv: bool,
        db_type: int,
        start_time: str,
        end_time: str,
        tz_code: str
) -> None:

    python_file = Path(__file__).name

    iana_name = US_TIME_ZONES.get(tz.upper())

    # Convert the input time strings to Apple Absolute Time
    # Handle the string -> Apple time conversion just one time, rather than
    # have seperate functions in each .py file
    start_time = Utils.convert_input_time_to_apple_time(start_time, iana_name)
    end_time = Utils.convert_input_time_to_apple_time(end_time, iana_name)


    # Get local time when the script begins
    t = time.localtime()
    ts = time.strftime("%d-%b-%Y at %H:%M:%S", t)
    
    # Print the local time when the script began
    console.print("Program started : [dodger_blue1]{ts)} ET")

    # Format the local time to append to the beginning of the output file name
    file_time = time.strftime("%Y-%m-%d_%H%M%S", t)

    if db == 1:
        from cache_sqlite_to_kml import (
            write_cache_sqlite_to_kml
        )
        write_cache_sqlite_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 2:
        from cache_encb_db_wifi_to_kml import (
            write_cache_encb_db_wifi_to_kml
        )
        write_cache_encb_db_wifi_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 3:
        from cache_encb_db_lte_to_kml import (
            write_cache_encb_db_lte_to_kml
        )
        write_cache_encb_db_lte_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 4:
        from cloud_v2_signif_loc_to_kml import (
            write_cache_v2_signif_loc_to_kml
        )
        write_cache_v2_signif_loc_to_kml(
            ppython_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 5:
        from local_signif_loc_visits_to_kml import (
            write_local_sqlite_signif_visits_to_kml
        )
        write_local_sqlite_signif_visits_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 6:
        from local_vehicle_loc_to_kml import (
            write_local_sqlite_vehicle_loc_to_kml
        )
        write_local_sqlite_vehicle_loc_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print_help()
    else:
        get_options()
