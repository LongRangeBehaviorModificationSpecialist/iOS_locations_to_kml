# !/usr/bin/env python3

from datetime import datetime, timezone
from rich.console import Console
from rich.prompt import Confirm
import pandas as pd
from pathlib import Path
import sqlite3
import sys
import webbrowser
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from shared.models import ConversionArgs
from vars.vars import US_TIME_ZONES

console = Console()


class Utils:

    @staticmethod
    def get_current_time() -> str:
        dt = datetime.now()
        time = dt.strftime("%H:%M:%S")
        # Pad to 6 then slice to 4
        microseconds = str(dt.microsecond).zfill(6)[:4]

        return f"{time}.{microseconds}"


    @staticmethod
    def query_database(source: Path | str, query: str):
        """Query the Cache.sqlite database file.

        Args:
            Path: path to the database to be queried
            query: query to run against the database

        Returns:
            Pandas dataframe from the database query.
        """
        # Connect to the database
        conn = sqlite3.connect(source)

        # Define your SQL query
        sql_query = query

        # Execute the query and load results into a DataFrame
        df = pd.read_sql_query(sql_query, conn)

        # Close the database connection
        conn.close()

        # Return the dataframe
        return df


    @staticmethod
    def generate_output_filename(base_filename: str = "results") -> str:
        """Generate a filename with the timestamp prefix"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return f"{timestamp}_{base_filename}.kml"


    @staticmethod
    def convert_timestamp_to_local(timestamp: int) -> str:
        """Converts a Cocoa Core Data timestamp to local time.

        Args:
            timestamp: A Cocoa Core Data timestamp, which is the number of
            seconds since midnight, January 1, 2001, GMT.

        Returns:
            A datetime object representing the local time equivalent of the
            given Cocoa Core Data timestamp.
        """
        # Convert the Cocoa Core Data timestamp to a Unix timestamp
        unix_timestamp: int = (int(timestamp) + 978307200)

        # Convert seconds since Unix epoch to datetime object
        dt_object = datetime.fromtimestamp(unix_timestamp)

        # Format datetime object to "%m-%d-%Y %H:%M:%S" format
        formatted_dt = dt_object.strftime("%a, %d-%b-%Y at %H:%M:%S")

        return formatted_dt


    @staticmethod
    def write_kml_closing() -> str:
        return """
        </Folder>
    </Document>
    </kml>"""


    @staticmethod
    def end_program(
        start_time: int,
        end_time: int,
        csv_file: str,
        count: int,
        kml_file: str,
        total_time: str,
        query_command_string: str,
    ) -> None:
        """Function used to display overall information about the records that
        were parsed from the database and the location of the output files
        within the file path.
        """

        # Display the time frame between which the records were obtained
        console.print(
            f"[magenta][{Utils.get_current_time()}][grey66] Processed "
            f"[blue]{count:,} [grey66]records from the database..."
        )
        console.print(
            f"[magenta][{Utils.get_current_time()}][grey66] Query "
            f"command:\n\n[i][blue]{query_command_string}[/i]\n"
        )
        console.print(
            f"[magenta][{Utils.get_current_time()}][grey66] Beginning "
            f"Date/Time Input (Local): [i][blue]"
            f"{Utils.convert_timestamp_to_local(start_time)}"
        )
        console.print(
            f"[magenta][{Utils.get_current_time()}][grey66] End Date/Time "
            f"Input (Local): [i][blue]"
            f"{Utils.convert_timestamp_to_local(end_time)}"
        )

        try:
            console.print(
                f"[magenta][{Utils.get_current_time()}][grey66] KML file: "
                f"[blue][i]{kml_file}"
            )
            if csv_file:
                console.print(
                    f"[magenta][{Utils.get_current_time()}][grey66] CSV "
                    f"file: [blue][i]{csv_file}"
                )
            else:
                pass
        except Exception as e:
            print(f"{e}")

        console.print(
            f"[magenta][{Utils.get_current_time()}][grey66] Task "
            f"completed in [blue]{total_time:.4f} [grey66]seconds"
        )

        return None


    @staticmethod
    def ask_open_kml_file(kml_file: Path | str) -> None:
        """Asks the user if they want to open the .kml file in Google Earth.

        If the user answers "y", then the .kml file is opened and this
        program is closed.

        If the user answers "n", then the this program is closed and no
        additional is taken.
        """

        open_choice = (
            Confirm.ask(
                f"[magenta][{Utils.get_current_time()}][yellow] Do you want "
                "to open the KML file now?",
            )
        )

        match open_choice:
            case "y":
                console.print(
                    f"[magenta][{Utils.get_current_time()}][grey66] Opening "
                    "the KML file..."
                )
                webbrowser.open(kml_file)
                return None
            case "n":
                console.print(
                    f"[magenta][{Utils.get_current_time()}][grey66] "
                    "Exiting now..."
                )
                sys.exit(0)


    @staticmethod
    def convert_input_time_to_apple_time(
            date_string: str,
            input_tz_name: str
    ) -> float:
        """Converts the time string to Apple Absolute Time based on the
        user-defined timezone.

        Args:
            date_string: Formatted as 'YYYY-MM-DD HHMMSS'
            input_tz_name: IANA timesone string (e.g., 'America/New_York'
                or 'UTC')
        """
        try:
            date_format = "%Y-%m-%d %H%M%S"
            # Parse the date_string into a native datetime
            native_dt = datetime.strptime(date_string, date_format)
            # Interpret the input datetime as Eastern Time
            input_dt = native_dt.replace(tzinfo=ZoneInfo(input_tz_name))
            # Convert input datetime to UTC
            utc_dt = input_dt.astimezone(timezone.utc)
            # Define Apple Epoch
            apple_epoch = datetime(2001, 1, 1, tzinfo=timezone.utc)
            # Calculate the difference in seconds between the input datetime
            # and the Apple Epoch time
            absolute_time = (utc_dt - apple_epoch).total_seconds()

            return absolute_time

        except ZoneInfoNotFoundError:
            return f"Error: '{input_tz_name}' is not a valid IANA timezone."
        except Exception as e:
            raise ValueError(
                f"Failed to convert time '{date_string}'. Please check the "
                f"input format -> {e}"
            )


    @staticmethod
    def create_conversion_args(args, from_interactive: bool = False):
        """Create ConversionArgs from either argparse or interactive input."""
        run_timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        if from_interactive:
            values = args
        else:
            values = vars(args)

        start_time_apple: float = 0.0
        end_time_apple: float = 0.0

        start_time_raw = values.get("start_time", "") or ""
        end_time_raw = values.get("end_time", "")
        iana_name = US_TIME_ZONES.get(
            values.get("tz_code", "UTC").upper()
        )

        if start_time_raw:
            # Convert the input time strings to Apple Absolute Time
            start_time_apple = Utils.convert_input_time_to_apple_time(
                start_time_raw,
                iana_name,
            )

        if end_time_raw:
            end_time_apple = Utils.convert_input_time_to_apple_time(
                end_time_raw,
                iana_name,
            )

        # Create dataclass (reuse same logic for both modes)
        try:
            conversion_args = ConversionArgs(
                python_file="make_kml.py",
                source=values["source"],
                dest=values["dest"],
                make_csv=values["make_csv"],
                db_type=values["db_type"],
                start_time=start_time_raw,
                end_time=end_time_raw,
                tz_code=values["tz_code"],
                start_time_apple=start_time_apple,
                end_time_apple=end_time_apple,
                run_timestamp=run_timestamp,
            )
            return conversion_args
        except (ValueError, KeyError) as e:
            console.print(f"[red]A validation error has occured -> {e}")
            exit(1)
