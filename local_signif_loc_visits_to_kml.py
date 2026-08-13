# !/usr/bin/env python3

from rich.console import Console
import time

from utils import Utils
from vars.local_signif_loc_visits import (
    local_signif_loc_visits_query,
    local_signif_loc_visits_kml_header,
    local_signif_loc_visits_kml_body
)

console = Console()

def write_local_sqlite_signif_visits_to_kml(
        python_file: str,
        source: str,
        dest: str,
        destf: str,
        make_csv: str,
        start_time: int,
        end_time: int,
        file_time: str
) -> None:

    # Time the program started
    file_start_time = time.perf_counter()

    query_command_string = f"""python .\{python_file} --source "{source}" \
--dest "{dest}" --destf "{destf}" --csv {make_csv} --db 5 --starttime \
{start_time} --endtime {end_time}"""

    # Generate the SQL query to include the start_time and end_time values.
    LOCAL_SIG_LOC_VISIT_QUERY = local_signif_loc_visits_query(
        start_time=start_time,
        end_time=end_time,
    )

    # Query the database file.
    df = Utils.query_database(source=source, query=LOCAL_SIG_LOC_VISIT_QUERY)

    # Get the total number of records in the worksheet.
    number_of_rows = len(df)

    # Print verification message to screen.
    console.print(
        f"\n[grey66]Found [blue]{number_of_rows:,} [grey66]rows "
        f"of data\n"
    )

    # Set output file to the correct format.
    kml_file = Utils.get_destf_name(
        dest=dest,
        destf=destf,
        time=file_time,
    )

    # Open the output file
    with open(kml_file, "w", encoding="utf-8") as f:

        # Write the header of the .kml file
        kml_header = local_signif_loc_visits_kml_header()

        f.write(kml_header)

        # Initialize a counter variable
        count = 0

        # Set variables from the dataframe
        for index, row in df.iterrows():
            record = row["record_number"]
            Z_PK = row["z_pk"]
            data_point_count = row["data_point_count"]
            location_of_interest_id = row["location_of_interest_id"]
            creation_date_utc = row["creation_date_utc"]
            entry_date_utc = row["entry_date_utc"]
            exit_date_utc = row["exit_date_utc"]
            expiration_date_utc = row["expiration_date_utc"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            location_horiz_uncertainty = row["location_horizontal_uncertainty"]
            location_confidence = row["location_confidence"]
            data_source = row["data_source"]

            # Print message to screen with each record number
            console.print(
                f"    [grey66]Processing Row #: [blue]{record:04d} "
                f"[grey66]| Z_PK #: [blue]{Z_PK}"
            )

            # Write the data from each record to the output .kml file.
            kml_body = local_signif_loc_visits_kml_body(
                record=record,
                data_point_count=data_point_count,
                location_of_interest_id=location_of_interest_id,
                creation_date_utc=creation_date_utc,
                entry_date_utc=entry_date_utc,
                exit_date_utc=exit_date_utc,
                expiration_date_utc=expiration_date_utc,
                latitude=latitude,
                longitude=longitude,
                location_horiz_uncertainty=location_horiz_uncertainty,
                location_confidence=location_confidence,
                data_source=data_source,
            )

            f.write(kml_body)

            # Increment the counter for the next record
            count += 1

        # Write the closing to the .kml file
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

    # Time the script completed
    ending_time = time.perf_counter()

    # Total time to complete
    total_time = ending_time - file_start_time

    Utils.end_program(
        query_command_string=query_command_string,
        number_of_rows=number_of_rows,
        start_time=start_time,
        end_time=end_time,
        csv_file=csv_file,
        count=count,
        kml_file=kml_file,
        total_time=total_time
    )

    # Ask user if they want to automatically open the output file.
    Utils.ask_open_kml_file(kml_file=kml_file)
