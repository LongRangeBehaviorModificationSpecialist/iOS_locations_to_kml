# !/usr/bin/env python3

import argparse
from argparse import RawDescriptionHelpFormatter
from datetime import datetime
import time
from utils import Utils
from pathlib import Path
from rich.console import Console
from rich.traceback import install

from shared.models import ConversionArgs
from shared.timezones import US_TIME_ZONES


from versions import (
    __version__,
    __author__,
    __last_updated__,
    get_version_string
)


# Create the console object
console = Console()
install(show_locals=True, console=console)


EXISTING_DATABASES = {
    "Cache.sqlite",
    "cache_encryptedB.db",
    "Cloud-V2.sqlite",
    "Local.sqlite",
}


def parse_args() -> argparse.Namespace:
    # Set up the argument parser syntax for the command line
    parser = argparse.ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        prog="make_kml_cli.py",
        usage="'%(prog)s --help' for more information",
        description=f"""
Description:
    make_kml_cli.py version {__version__}

Author:
    {__author__}

Last Updated:
    {__last_updated__}

Description
    Create a .kml file by reading the location records from the database \
specified in the '--db_type' option.

    The '--start_time' and '--end_time' values can be given as a string using \
the following format: 'YYYY-MM-DD HHMMSS'.

URL
    github.com/LongRangeBehaviorModificationSpecialist/ios_locations_to_kml

Example
    python .\\make_kml.py --source [SOURCE_FILE] --dest [DESTINATION_FOLDER] \
[--make_csv | None] --db_type [DATABASE_CHOICE] --start_time \
"[YYYY-MM-DD HHMMSS]" --end_time "[YYYY-MM-DD HHMMSS]" --tz_code "[TIMEZONE]"

Notes
    Enclose the full path in double quotes if it contains spaces."""
)

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="[str] Full path of database file"
    )

    parser.add_argument(
        "--dest",
        type=Path,
        required=True,
        help="[str] Output directory"
    )

    parser.add_argument(
        "--make_csv",
        required=False,
        action="store_true",
        help="[str] Save a .csv file containing the query results?"
    )

    parser.add_argument(
        "--db_type",
        type=str,
        required=True,
        choices=["1", "2", "3", "4", "5", "6"],
        help="""[int] Type of location data you want to examine. Enter the \
corresponding number for the database/table containing the records you want \
to examine:
1 = Cache.sqlite (Location History);
2 = cache_encryptedB.db (WiFi locations);
3 = cache_encryptedB.db (LTE locations);
4 = Cloud-V2.sqlite (Significant Locations);
5 = Local.sqlite (Significant Location Visits); or
6 = Local.sqlite (Vehicle Locations)."""
    )

    parser.add_argument(
        "--start_time",
        type=str,
        required=True,
        help="[str] Timestamp of the first record to get ('YYYY-MM-DD HHMMSS')."
    )

    parser.add_argument(
        "--end_time",
        type=str,
        required=True,
        help="[str] Timestamp of the last record to get ('YYYY-MM-DD HHMMSS')."
    )

    parser.add_argument(
        "--tz_code",
        type=str,
        required=True,
        choices=["ET", "CT", "MT", "AZ", "PT", "AKT", "HT", "UTC"],
        help="[str] Timezone used for the time values."
    )

    return parser.parse_args()


def validate_source(source_path: Path) -> bool:
    """Check if source is in database list."""
    if source_path.name in EXISTING_DATABASES:
        console.print(
            f"[magenta][{Utils.get_current_time()}][green3] Database "
            f"file: '{source_path.name}' is in the database file list. "
            "Continuing..."
        )
        return True
    else:
        console.print(
            f"[magenta][{Utils.get_current_time()}][yellow] Warning: "
            f"'{source_path.name}' is NOT in the known database file list."
        )
        return False


def dispatch_converter(conversion_args: ConversionArgs, db_type: str) -> None:
    """Route all conversions through unified writer."""
    from writer import write_cache_to_kml
    write_cache_to_kml(conversion_args)


def main() -> None:

    args = parse_args()

    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    source_path = Path(args.source)
    validate_source(source_path)

    iana_name = US_TIME_ZONES.get(args.tz_code.upper())

    start_time_apple = None
    end_time_apple = None

    if args.start_time:
    # Convert the input time strings to Apple Absolute Time
        start_time_apple = Utils.convert_input_time_to_apple_time(
            args.start_time,
            iana_name,
        )
        end_time_apple = Utils.convert_input_time_to_apple_time(
            args.end_time,
            iana_name,
        )

    run_time = time.strftime("%d-%b-%Y at %H:%M:%S", time.localtime())
    # Print the local time when the script began
    console.print(
        f"[magenta][{Utils.get_current_time()}][grey66] Program started: "
        f"[dodger_blue1]{run_time}"
    )

    # Create the dataclass from argparse.Namespace
    conversion_args = ConversionArgs(
        python_file = Path(__file__).name,
        source=args.source,
        dest=args.dest,
        make_csv=args.make_csv,
        db_type = args.db_type,
        start_time=args.start_time,
        end_time=args.end_time,
        tz_code=args.tz_code,
        start_time_apple=start_time_apple or 0.0,
        end_time_apple=end_time_apple,
        run_timestamp=run_timestamp,
    )

    # Route to converter
    dispatch_converter(conversion_args, args.db_type)


if __name__ == "__main__":
    main()
