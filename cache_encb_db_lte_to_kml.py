# !/usr/bin/env python3

from rich.console import Console
import time

from functions.functions import Utils
from vars.cache_encb_lte import(
    cache_encb_db_lte_query,
    cache_encb_db_lte_kml_file_header,
    cache_encb_db_lte_kml_file_body
)

c = Console()

def write_cache_encb_db_lte_to_kml(
        python_file: str,
        source: str,
        dest: str,
        destf: str,
        make_csv: str,
        start_time: int,
        end_time: int,
        file_time: str
) -> None:

    # Get the time the program began
    file_start_time = time.perf_counter()

    query_command_string = (f"""
python .\{python_file} --source "{source}" --dest "{dest}" --destf "{destf}" \
--csv {make_csv} --db 3 --starttime {start_time} --endtime {end_time}"""
    )

    # Generate the SQL query
    CACHE_ENCRYPTEDB_WIFI_QUERY = cache_encb_db_lte_query(
        start_time=start_time,
        end_time=end_time,
    )

    # Query the database file
    df = Utils.query_database(source=source, query=CACHE_ENCRYPTEDB_WIFI_QUERY)

    # Get the total number of records
    number_of_rows = len(df)

    # Print verification message to screen
    c.print(
        f"\n[grey66]Found [dodger_blue1]{number_of_rows:,} [grey66]rows "
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

        # Write the header block of .kml file
        kml_header = cache_encb_db_lte_kml_file_header()

        f.write(kml_header)

        # Initialize a counter variable
        count = 0

        # Set variables from the dataframe
        for index, row in df.iterrows():
            record = row["record_number"]
            utc_time = row["timestamp_utc"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            mcc = row["mcc"]
            mnc = row["mnc"]
            tac = row["tac"]
            ci = row["ci"]
            horiz_accuracy = row["horizontal_accuracy"]
            altitude = row["altitude"]
            confidence = row["confidence"]
            data_source = row["data_source"]

            # Print message to screen with each record number added
            c.print(
                f"    [grey66]Processing Row # : [dodger_blue1]{record:04d}"
            )

            site_info = f"mcc: {mcc} | mnc: {mnc} | tac: {tac} | ci: {ci}"

            # Write the data from each record to the .kml file
            kml_body = cache_encb_db_lte_kml_file_body(
                record=record,
                utc_time=utc_time,
                latitude=latitude,
                longitude=longitude,
                site_info=site_info,
                horiz_accuracy=horiz_accuracy,
                altitude=altitude,
                confidence=confidence,
                data_source=data_source,
            )

            f.write(kml_body)

            # Increment the counter variable
            count += 1

        # Write the closing block to the .kml file
        f.write(f"{Utils.write_kml_closing()}")

    # If the user chose to save a .csv file
    match make_csv:
        case "y":
            csv_file = Utils.get_csv_file_name(
                dest=dest,
                destf=destf,
                time=file_time,
            )
            df.to_csv(output_csv_file, index=False)
        case "n":
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
        total_time=total_time,
    )

    # Ask user if they want to open the output file
    Utils.ask_open_kml_file(kml_file=kml_file)

