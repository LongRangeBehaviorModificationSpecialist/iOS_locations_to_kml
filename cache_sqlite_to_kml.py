# !/usr/bin/env python3

from rich.console import Console
import time

from make_kml_cli import ConversionArgs
from functions.functions import Utils
from vars.cache_sqlite import (
    cache_sqlite_query,
    cache_sqlite_kml_file_header,
    cache_sqlite_kml_file_body
)


c = Console()


def write_cache_sqlite_to_kml(args: ConversionArgs) -> None:

    # Time the program began
    file_start_time = time.perf_counter()

    query_command_string = (
        f"python .\{python_file} --source '{source}' --dest '{dest}' --destf "
        f"'{destf}' --csv '{make_csv}' --db 1 --starttime '{start_time}' --endtime "
        f"'{end_time}'"
    )

    # Generate the SQL query
    CACHE_SQLITE_QUERY = cache_sqlite_query(
        start_time=start_time,
        end_time=end_time,
    )

    # Query the database
    df = Utils.query_database(source=source, query=CACHE_SQLITE_QUERY)

    # Get the total number of records returned
    number_of_rows = len(df)

    # Print verification message to screen
    c.print(
        f"\n[grey66]Found [dodger_blue1]{number_of_rows:,} [grey66]rows "
        "of data\n"
    )

    # Set .kml file name
    kml_file = Utils.get_destf_name(
        dest=dest,
        destf=destf,
        time=file_time,
    )

    # Open the output file
    with open(kml_file, "w", encoding="utf-8") as f:

        # Write the header block of the .kml file
        kml_header = cache_sqlite_kml_file_header()

        f.write(kml_header)

        # Initialize a counter variable
        count = 0

        # Set variables from the dataframe
        for index, row in df.iterrows():
            record = row["record_number"]
            Z_PK = row["z_pk"]
            utc_time = row["timestamp_utc"]
            local_time = row["timestamp_local"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            loc_combined = row["gps_merged"]
            speed_meters_per_sec = row["speed_meters_sec"]
            speed_mph = row["speed_mph"]
            course = row["course"]
            horiz_acc_meters = row["horiz_accuracy_meters"]
            horiz_acc_feet = row["horiz_accuracy_feet"]
            vert_acc_meters = row["vertical_accuracy_meters"]
            vert_acc_feet = row["vertical_accuracy_feet"]
            data_source = row["data_source"]

            # Print message to screen with each record number
            c.print(
                f"    [grey66]Processing Row #: [dodger_blue1]{record:04d} "
                "[grey66]| Z_PK #: [dodger_blue1]{Z_PK}"
            )

            # Write the data from each record to the .kml file
            kml_body = cache_sqlite_kml_file_body(
                record=record,
                local_time=local_time,
                latitude=latitude,
                longitude=longitude,
                loc_combined=loc_combined,
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
    match make_csv:
        case "y":
            csv_file = Utils.get_csv_file_name(
                dest=dest,
                destf=destf,
                time=file_time,
            )
            df.to_csv(csv_file, index=False)
        case "n":
            pass

    # Time the script completed
    ending_time = time.perf_counter()

    # Get the total time
    total_time = ending_time - file_start_time

    Utils.end_program(
        query_command_string=query_command_string,
        number_of_rows=number_of_rows,
        start_time=start_time,
        end_time=end_time,
        csv_file=csv_file,
        count=count,
        kml_file=kml_file,
        total_time=total_time,
    )

    # Ask user if they want to open the .kml file
    Utils.ask_open_kml_file(kml_file=kml_file)
