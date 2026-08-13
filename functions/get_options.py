# !/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.traceback import install
from typing import Dict

from vars.vars import EXISTING_DATABASES, DATABASE_IDS
from utils import Utils


console = Console()
install(show_locals=True, console=console)


db_option_list = {
    "1": "Cache.sqlite (Location History)",
    "2": "cache_encryptedB.db (WiFi locations)",
    "3": "cache_encryptedB.db (LTE locations)",
    "4": "Cloud-V2.sqlite (Significant Locations)",
    "5": "Local.sqlite (Significant Location Visits)",
    "6": "Local.sqlite (Vehicle Locations)"
}

def get_source() -> Path:
    """Get and return the source path of the database to analyze."""
    while True:
        source = Prompt.ask(
            f"\n[magenta][{Utils.get_current_time()}][grey66] Enter the file "
            "path to the database"
        ).strip("\"'")
        source = Path(source).resolve()
        console.print(
            f"[magenta][{Utils.get_current_time()}][blue] Path to database "
            f"file was entered as -> [magenta][i]{source}"
        )

        if source.name in EXISTING_DATABASES:
            console.print(
                f"\n[magenta][{Utils.get_current_time()}][green] Database "
                f"file [magenta][i]{source.name}[/i][/] is in the known file "
                "list. Continuing..."
            )
            return Path(source)
        else:
            console.print(
                f"\n[magenta][{Utils.get_current_time()}][red] Database "
                f"file [magenta][i]{source.name}[/i][/] is not in the known "
                "file list. Please choose a different file..."
            )


def get_dest() -> Path:
    """Get and return the destination path to save the results file(s)."""
    dest = Prompt.ask(
        f"\n[magenta][{Utils.get_current_time()}][grey66] Enter the file "
        "path where results will be saved"
    ).strip("\"'")

    console.print(
        f"[magenta][{Utils.get_current_time()}][blue] Results will be saved "
        f"in the [magenta][i]{dest}[/i][/] directory"
    )
    return Path(dest)


def get_make_csv() -> str:
    """Get and return the option to create a .csv file with the results."""
    while True:
        csv_option = Prompt.ask(
            f"\n[magenta][{Utils.get_current_time()}][grey66] Create a CSV "
            "file with the results of the query?",
            choices=["y", "n"],
            show_choices=True,
            default="y",
        ).strip().lower()

        if csv_option == "y":
            console.print(
                f"[magenta][{Utils.get_current_time()}][blue] A CSV file "
                f"[magenta][i]WILL[/i][/] be created with the KML file"
            )
            return True
        elif csv_option == "n":
            console.print(
                f"[magenta][{Utils.get_current_time()}][blue] A CSV file "
                f"[magenta][i]WILL NOT[/i][/] be created"
            )
            return False
        else:
            console.print(
                f"[magenta][{Utils.get_current_time()}][yellow] A valid option "
                "was not entered. Try again."
            )


def get_db_type() -> int:
    """Get and return the specific location option to examine."""
    while True:
        try:
            db_type = Prompt.ask(
                f"\n[magenta][{Utils.get_current_time()}][grey66] Type of "
                f"location data to examine (see help menu for options)",
                choices=["1", "2", "3", "4", "5", "6"],
                show_choices=True
            ).strip()

            if db_type in DATABASE_IDS:
                console.print(
                    f"[magenta][{Utils.get_current_time()}][blue] ✓ Type of "
                    f"location data to be examined -> [magenta][i]"
                    f"{DATABASE_IDS[db_type]}"
                )
            return db_type
        except ValueError:
            # Handles where input cannot be converted to an integer
            console.print(
                f"[magenta][{Utils.get_current_time()}][yellow] ✗ Error -> "
                "Invalid input. Please enter a valid number"
            )
        except KeyError:
            # Handles where the number is an integer, but not in dictionary
            console.print(
                f"[magenta][{Utils.get_current_time()}][yellow] ✗ Error -> "
                f"Number [magenta][i]{db_type}[/i][/] does not match any "
                f"available options"
            )


def get_start_time() -> str:
    """Get and return the date/time of the first record to return
    from the query.
    """
    try:
        start_time = Prompt.ask(
            f"\n[magenta][{Utils.get_current_time()}][grey66] Enter the "
            "date/time of the [i]first[/i] record to be returned (use "
            "'YYYY-MM-DD HHMMSS' format)"
        )
        # Convert the input string to datetime object
        datetime.strptime(start_time, "%Y-%m-%d %H%M%S")
        console.print(
            f"[magenta][{Utils.get_current_time()}][blue] Date/Time of "
            f"[i]first[/i] record to be returned -> [magenta][i]"
            f"{start_time}"
        )
        return start_time
    except ValueError as e:
        console.print(f"[red1]An error occured -> {e}")
        get_start_time()


def get_end_time() -> str:
    """Get and return the date/time of the last record to return
    from the query.
    """
    try:
        end_time = Prompt.ask(
            f"\n[magenta][{Utils.get_current_time()}][grey66] Enter the "
            f"date/time of the [i]last[/i] record to be returned (use "
            f"'YYYY-MM-DD HHMMSS' format)"
        )
        if datetime.strptime(end_time, "%Y-%m-%d %H%M%S"):
            console.print(
                f"[magenta][{Utils.get_current_time()}][blue] Date/Time of "
                f"[i]last[/i] record to be returned -> [magenta]"
                f"[i]{end_time}"
            )
            return end_time
        else:
            raise ValueError
    except ValueError as e:
        console.print(
            f"[magenta][{Utils.get_current_time()}][yellow] An error occured "
            f"-> {e}"
        )
        get_end_time()


def get_tz_code() -> str:
    """Get and return the timezone of the start and end times input
    by the user.
    """
    tz_code = Prompt.ask(
        f"\n[magenta][{Utils.get_current_time()}][grey66] Enter the timezone "
        "used for the date/time values"
    )
    console.print(
        f"[magenta][{Utils.get_current_time()}][blue] Recorded timezone "
        f"value is -> [magenta][i]{tz_code}"
    )
    return tz_code


def get_interactive_values() -> Dict[str, str | int]:
    """Handle the functions to get all of the options from the prompts that
    are presented to the user.
    """
    values = {}

    console.print("")
    console.print(
        Panel.fit(
            # "[bold][cyan]Make .kml from database file[/bold][grey66]\n"
            "\n[dim]Please answer the following questions to configure the "
            "application\n",
            border_style="cyan",
            title="Make .kml from database file"
        )
    )

    values["source"] = get_source()
    values["dest"] = get_dest()
    values["make_csv"] = get_make_csv()
    values["db_type"] = get_db_type()
    values["start_time"] = get_start_time()
    values["end_time"] = get_end_time()
    values["tz_code"] = get_tz_code()

    return values
