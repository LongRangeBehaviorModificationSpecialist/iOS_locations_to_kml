# !/usr/bin/env python3

import argparse
from argparse import RawDescriptionHelpFormatter
import time
from utils import Utils
from pathlib import Path
from rich.console import Console
from rich.traceback import install

from functions.get_options import get_interactive_values
from shared.models import ConversionArgs
from vars.vars import EXISTING_DATABASES


from versions import (
    __version__,
    __author__,
    __last_updated__,
)

#TODO -- add option #7 for the 'ZRTLEARNEDLOCATIONOFINTERESTMO' table from Local.sqlite
#TODO -- add option #8 for the 'ZRTLEARNEDLOCATIONOFINTERESTTRANSITIONMO' table from Local.sqlite

# Create the console object
console = Console()
install(show_locals=True, console=console)


def parse_args() -> argparse.Namespace:
    # Set up the argument parser syntax for the command line
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: RawDescriptionHelpFormatter(
            prog, max_help_position=75
        ),
        prog="make_kml_cli.py",
        usage="'%(prog)s --help' for more information",
        description=(f"""
Description:
    make_kml.py (version {__version__})

Author:
    {__author__}

Last Updated:
    {__last_updated__}

Description:
    Create a .kml file by reading the location records from the iOS database
    file specified in the '--db_type' option.

    The '--start_time' and '--end_time' values must be given as a string
    using the following format: "YYYY-MM-DD HHMMSS". (Enclose data in quotes.)

    The databases and tables (for the 'db_type' option) with location
    information are listed below

    1 = Cache.sqlite (Location History),
    2 = cache_encryptedB.db (WiFi locations),
    3 = cache_encryptedB.db (LTE locations),
    4 = Cloud-V2.sqlite (Significant Locations),
    5 = Local.sqlite (Significant Location Visits),
    6 = Local.sqlite (Vehicle Locations),
    7 = Local.sqlite (Locations of Interest) [*PENDING*], or
    8 = Local.sqlite (Locations of Interest Transitions) [*PENDING*]

    Valid options for the '--tz_code' parameter are:

    "ET"  = "America/New_York"
    "CT"  = "America/Chicago"
    "MT"  = "America/Denver"
    "AZ"  = "America/Phoenix" (no DST)
    "PT"  = "America/Los_Angeles"
    "AKT" = "America/Anchorage"
    "HT"  = "Pacific/Honolulu"
    "UTC" = UTC timezone

URL:
    github.com/LongRangeBehaviorModificationSpecialist/ios_locations_to_kml

Example:
    python .\make_kml.py [-i | --interactive | None] --source <str> --dest \
<str> [--make_csv | None] --db_type <str> --start_time <"YYYY-MM-DD HHMMSS"> \
--end_time <"YYYY-MM-DD HHMMSS"> --tz_code <str>

Notes:
    Enclose file paths in double quotes (for the '--source' and '--dest' values)
    if it contains spaces."""
        )
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        required=False,
        help="Run in interactive mode (prompt for each value)"
    )

    parser.add_argument(
        "--source",
        type=Path,
        required=False,
        help="Full path of database file"
    )

    parser.add_argument(
        "--dest",
        type=Path,
        required=False,
        help="Output directory"
    )

    parser.add_argument(
        "--make_csv",
        required=False,
        action="store_true",
        help="Save a CSV file containing the query results?"
    )

    parser.add_argument(
        "--db_type",
        type=str,
        required=False,
        choices=["1", "2", "3", "4", "5", "6"],
        help="Number associated with the database/table you want to query"
    )


    parser.add_argument(
        "--start_time",
        type=str,
        required=False,
        help="Timestamp of the first record to get (\"YYYY-MM-DD HHMMSS\")"
    )

    parser.add_argument(
        "--end_time",
        type=str,
        required=False,
        help="Timestamp of the last record to get (\"YYYY-MM-DD HHMMSS\")"
    )

    parser.add_argument(
        "--tz_code",
        type=str,
        required=False,
        choices=["ET", "CT", "MT", "AZ", "PT", "AKT", "HT", "UTC"],
        help="Timezone used for the entered time values"
    )

    return parser.parse_args()


def validate_source(source_path: Path) -> bool:
    """Check if source is in database list."""
    if source_path.name in EXISTING_DATABASES:
        console.print(
            f"[magenta][{Utils.get_current_time()}][bright_green] Database "
            f"file → '{source_path.name}' is in the database file list. "
            "Continuing..."
        )
        return True
    else:
        console.print(
            f"[magenta][{Utils.get_current_time()}][bright_yellow] Warning → "
            f"'{source_path.name}' is NOT in the known database file list."
        )
        return False


def dispatch_converter(
        conversion_args: ConversionArgs,
        db_type: str
) -> None:
    """Route all conversions through unified writer."""
    from writer import write_cache_to_kml
    write_cache_to_kml(conversion_args)


def main() -> None:

    args = parse_args()

    run_time = time.strftime("%d-%b-%Y at %H:%M:%S", time.localtime())
    # Print the local time when the script began
    console.print(
        f"[magenta][{Utils.get_current_time()}][grey66] Program started: "
        f"[blue]{run_time}"
    )

    if args.interactive:
        console.print(
            f"[magenta][{Utils.get_current_time()}][bright_yellow] Starting "
            "INTERACTIVE mode..."
        )
        interactive_values = get_interactive_values()
        conversion_args = Utils.create_conversion_args(
            interactive_values,
            from_interactive=True,
        )
    else:
        # Validate required CLI args
        if not args.source or not args.end_time or not args.dest:
            console.print(
                f"[magenta][{Utils.get_current_time()}][bright_yellow] ERROR → "
                f"Missing required arguments.\n"
                "[grey66]Run with '--interactive' ('-i') to enter values "
                "interactively or use '--help' for more information"
            )
            exit(1)

        conversion_args = Utils.create_conversion_args(
            args,
            from_interactive=False,
        )

    # Route to converter
    dispatch_converter(conversion_args, args.db_type)


if __name__ == "__main__":
    main()
