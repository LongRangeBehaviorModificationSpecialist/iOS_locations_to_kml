# !/usr/bin/env python3

from rich.console import Console
from rich.traceback import install
import time

from make_kml import ConversionArgs
from utils import Utils
from vars.cache_sqlite import (
    cache_sqlite_query,
    cache_sqlite_kml_header,
    cache_sqlite_kml_body
)


console = Console()
install(show_locals=True, console=console)


def write_cache_sqlite_to_kml(args: ConversionArgs) -> None:
    """Convert SQLite cache to KML format (optionally CSV too).

    Args:
        Take the ConversionArgs dataclass as an argument.
    """

    # Time the program began
    file_start_time = time.perf_counter()

    query_command_string = f"""python .\{args.python_file} --source \
"{args.source}" --dest "{args.dest}" --make_csv {args.make_csv} --db_type 1 \
--starttime {args.start_time} --endtime {args.end_time} --tz_code {args.tz_code}"""

    # Generate the SQL query
    CACHE_SQLITE_QUERY = cache_sqlite_query(
        start_time=args.start_time_apple,
        end_time=args.end_time_apple,
    )

    # Query the database
    df = Utils.query_database(source=args.source, query=CACHE_SQLITE_QUERY)

    # Get the total number of records returned
    number_of_rows = len(df)

    # Print verification message to screen
    console.print(
        f"\n[grey66]Found [blue]{number_of_rows:,} [grey66]rows "
        "of data\n"
    )

    kml_file = args.kml_file_path
    kml_file.parent.mkdir(parents=True, exist_ok=True)

    console.print(f"[grey66]Writing data to: {kml_file}\n")


    # Open the output file
    with open(kml_file, "w", encoding="utf-8") as f:

        # Write the header block of the .kml file
        kml_header = cache_sqlite_kml_header()

        f.write(kml_header)

        # Initialize a counter variable
        count = 0

        # Set variables from the dataframe
        for index, row in df.iterrows():
            record = row["record_number"],
            Z_PK = row["z_pk"],
            utc_time = row["timestamp_utc"],
            local_time = row["timestamp_local"],
            latitude = row["latitude"],
            longitude = row["longitude"],
            gps_merged = row["gps_merged"],
            speed_meters_per_sec = row["speed_meters_sec"],
            speed_mph = row["speed_mph"],
            course = row["course"],
            horiz_acc_meters = row["horiz_accuracy_meters"],
            horiz_acc_feet = row["horiz_accuracy_feet"],
            vert_acc_meters = row["vertical_accuracy_meters"],
            vert_acc_feet = row["vertical_accuracy_feet"],
            data_source = row["data_source"],

            # Print message to screen with each record number
            console.print(
                f"    [grey66]Processing Row #: [blue]{record:04d} "
                f"[grey66]| Z_PK #: [blue]{Z_PK}"
            )

            # Write the data from each record to the .kml file
            kml_body = cache_sqlite_kml_body(
                record=record,
                local_time=local_time,
                latitude=latitude,
                longitude=longitude,
                gps_merged=gps_merged,
                course=course,
                horiz_acc_meters=horiz_acc_meters,
                utc_time=utc_time,
                speed_meters_per_sec=speed_meters_per_sec,
                speed_mph=speed_mph,
                horiz_acc_feet=horiz_acc_feet,
                vert_acc_meters=vert_acc_meters,
                vert_acc_feet=vert_acc_feet,
                data_source=data_source,
            )

            f.write(kml_body)

            # Increment the counter variable
            count += 1

        # Write the closing block of the .kml file
        f.write(f"{Utils.write_kml_closing()}")

    # If the user chose to save a .csv file
    if args.make_csv:
        df.to_csv(args.csv_file_path, index=False)

    # Time the script completed
    ending_time = time.perf_counter()

    # Get the total time
    total_time = ending_time - file_start_time

    Utils.end_program(
        query_command_string=query_command_string,
        number_of_rows=number_of_rows,
        start_time=args.start_time,
        end_time=args.end_time,
        csv_file=args.csv_file_path,
        count=count,
        kml_file=kml_file,
        total_time=total_time,
    )

    # Ask user if they want to open the .kml file
    Utils.ask_open_kml_file(kml_file=kml_file)
