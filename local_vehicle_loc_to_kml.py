# !/usr/bin/env python3

from rich.console import Console
import time

from utils import Utils
from vars.local_vehicle_loc import (
    local_vehicle_loc_query,
    local_vehicle_loc_kml_header,
    local_vehicle_loc_kml_body
)

console = Console()

def write_local_sqlite_vehicle_loc_to_kml(
        python_file: str,
        source: str,
        dest: str,
        destf: str,
        make_csv: str,
        start_time: int,
        end_time: int,
        file_time: str
) -> None:

    # Time the program
    file_start_time = time.perf_counter()

    query_command_string = f"""python .\{python_file} --source "{source}" \
--dest "{dest}" --destf "{destf}" --csv {make_csv} --db 6 --starttime \
{start_time} --endtime {end_time}"""

    # Generate the SQL query
    LOCAL_SQLITE_VEH_LOC_QUERY = local_vehicle_loc_query(
        start_time=start_time,
        end_time=end_time,
    )

    # Query the database file
    df = Utils.query_database(source=source, query=LOCAL_SQLITE_VEH_LOC_QUERY)

    # Get the total number of records returned
    number_of_rows = len(df)

    # Print verification message to screen
    console.print(
        f"\n[grey66][-] Found [dodger_blue1]{number_of_rows:,} [grey66]rows "
        f"of data\n"
    )

    # Set output file to the correct format
    kml_file = Utils.get_destf_name(
        dest=dest,
        destf=destf,
        time=file_time,
    )

    # Open the output file
    with open(kml_file, "w", encoding="utf-8") as f:

        # Write the header block of the .kml file
        kml_header = local_vehicle_loc_kml_header()

        f.write(kml_header)

        # Initialize a counter variable
        count = 0

        # Set variables from the dataframe
        for index, row in df.iterrows():
            record = row["record_number"]
            Z_PK = row["z_pk"]
            utc_time = row["date_time_utc"]
            location_time_utc = row["location_date_utc"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            location_uncertainty = row["location_uncertainty"]
            identifier = row["identifier"]
            data_source = row["data_source"]

            # Print message to screen with each record number added
            console.print(
                f"    [grey66]Processing Row #: [dodger_blue1]{record:04d} "
                f"[grey66]| Z_PK #: [dodger_blue1]{Z_PK}"
            )

            # Write the data from each record to the .kml file
            kml_body = local_vehicle_loc_kml_body(
                record=record,
                utc_time=utc_time,
                location_time_utc=location_time_utc,
                latitude=latitude,
                longitude=longitude,
                location_uncertainty=location_uncertainty,
                identifier=identifier,
                data_source=data_source
            )

            f.write(kml_body)

            # Increment the counter variable
            count += 1

        # Write the closing block to the .kml file
        f.write(f"{Utils.write_kml_closing()}")

    # If the user chose to save a .csv file
    if make_csv.lower() == "y":
        csv_file = Utils.get_csv_file_name(
            dest=dest,
            destf=destf,
            time=file_time,
        )
        df.to_csv(csv_file, index=False)
    else:
        pass

    # Time the script finished
    ending_time = time.perf_counter()

    # Total time the to complete
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

    # Ask user if they want to open the output file
    Utils.ask_open_kml_file(kml_file=kml_file)
