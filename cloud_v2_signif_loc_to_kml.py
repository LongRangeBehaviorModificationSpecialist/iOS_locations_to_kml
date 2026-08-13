# !/usr/bin/env python3

from rich.console import Console
import time

from utils import Utils
from vars.cloud_v2_signif_loc import (
    cloud_v2_signif_loc_query,
    cloud_v2_signif_loc_kml_header,
    cloud_v2_signif_loc_kml_body
)

console = Console()

def write_cache_v2_signif_loc_to_kml(
        python_file: str,
        source: str,
        dest: str,
        destf: str,
        make_csv: str,
        start_time: int,
        end_time: int,
        file_time: str
) -> None:

    # Time the program began
    file_start_time = time.perf_counter()

    # Reconstruct the command line entry
    query_command_string = f"""python .\{python_file} --source "{source}" \
--dest "{dest}" --destf "{destf}" --csv {make_csv} --db 4 --starttime \
{start_time} --endtime {end_time}"""

    # Generate the SQL query
    CLOUDV2_SIG_LOC_QUERY = cloud_v2_signif_loc_query(
        start_time=start_time,
        end_time=end_time,
    )

    # Query the database
    df = Utils.query_database(source=source, query=CLOUDV2_SIG_LOC_QUERY)

    # Get the total number of records returned
    number_of_rows = len(df)

    # Print verification message to screen
    console.print(
        f"\n[grey66]Found [blue]{number_of_rows:,} [grey66]rows "
        "of data\n"
    )

    # Set the .kml file name
    kml_file = Utils.get_destf_name(
        dest=dest,
        destf=destf,
        time=file_time,
    )

    # Open the output file
    with open(kml_file, "w", encoding="utf-8") as f:

        # Write the header block to the .kml file
        kml_header = cloud_v2_signif_loc_kml_header()

        f.write(kml_header)

        # Initialize a counter variable
        count = 0

        # Set variables from the dataframe
        for index, row in df.iterrows():
            record = row["record_number"]
            Z_PK = row["z_pk"]
            address_info = row["address_info"]
            probable_place_name = row["probable_place_name"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            uncertainty = row["uncertainty"]
            add_create_utc = row["address_creation_date_utc"]
            add_expire_utc = row["address_expire_date_utc"]
            data_source = row["data_source"]

            # Print message to screen with each record number
            console.print(
                f"    [grey66]Processing Row #: [blue]{record:04d} "
                f"[grey66]| Z_PK #: [blue]{Z_PK}"
            )

            # Write the data from each record to the .kml file
            kml_body = cloud_v2_signif_loc_kml_body(
                record=record,
                Z_PK=Z_PK,
                address_info=address_info,
                probable_place_name=probable_place_name,
                latitude=latitude,
                longitude=longitude,
                uncertainty=uncertainty,
                add_create_utc=add_create_utc,
                add_expire_utc=add_expire_utc,
                data_source=data_source,
            )

            f.write(kml_body)

            # Increment the counter variable
            count += 1

        # Write the closing block to the .kml file
        f.write(f"{Utils.write_kml_closing()}")

    # If the user choose to save a .csv file
    if make_csv.lower() == "y":
        csv_file = Utils.get_csv_file_name(
            dest=dest,
            destf=destf,
            time=file_time,
        )
        df.to_csv(csv_file, index=False)
    else:
        pass

    # Time the script ended
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
        total_time=total_time,
    )

    # Ask user if they want to open the .kml file
    Utils.ask_open_kml_file(kml_file=kml_file)
