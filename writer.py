# !/usr/bin/env python3

from rich.console import Console
from rich.prompt import Prompt
from rich.traceback import install
import time
from handlers import get_handlers
from shared.models import ConversionArgs
from utils import Utils


console = Console()
install(show_locals=True, console=console)


def write_cache_to_kml(args: ConversionArgs) -> None:
    """Convert database cache to KML format (optionally CSV too).

    Handles all database types via the handler registry. The specific
    query, header, row extraction, and body writing logic for each
    db_type is defined in handlers.py.

    Args:
        args: ConversionArgs dataclass containing all configuration.
    """

    # Get handlers for this db_type (raises error if invalid)
    handlers = get_handlers(args.db_type)

    # Time the program
    file_start_time = time.perf_counter()

    # Generate query command string
    query_command_string = (
        f"python .\\{args.python_file} --source \"{args.source}\" "
        f"--dest \"{args.dest}\" --make_csv {args.make_csv} "
        f"--db_type {args.db_type} "
        f"--start_time \"{args.start_time}\" --end_time \"{args.end_time}\" "
        f"--tz_code \"{args.tz_code}\""
    )

    query = handlers["query"](
        start_time=args.start_time_apple,
        end_time=args.end_time_apple,
    )

    df = Utils.query_database(source=args.source, query=query)

    # Print verification message
    number_of_rows = len(df)

    console.print(
        f"[magenta][{Utils.get_current_time()}][grey66] The initial query "
        f"found [dodger_blue1]{number_of_rows:,} [grey66]rows of data"
    )

    # ===== USER CONFIRMATION PROMPT =====
    try:
        user_input = Prompt.ask(
            f"[magenta][{Utils.get_current_time()}][yellow3] Do you want "
            "to continue writing the KML file?",
            choices=["y", "n"],
            show_choices=True,
            default="y"
        ).strip().lower()
    except KeyboardInterrupt:
        console.print(
            f"[magenta][{Utils.get_current_time()}][red1] Operation "
            "cancelled by user."
        )
        return

    if user_input not in ("y"):
        console.print(
            f"[magenta][{Utils.get_current_time()}][red1] Operation "
            "cancelled by user. No files written."
        )
        return

    # Setup output file
    kml_file = args.kml_file_path
    kml_file.parent.mkdir(parents=True, exist_ok=True)
    console.print(
        f"[magenta][{Utils.get_current_time()}][grey66] Writing data to: "
        f"[dodger_blue1]{kml_file.name}"
    )

    # Open output file
    with open(kml_file, "w", encoding="utf-8") as f:
        kml_header = handlers["header"]()
        f.write(kml_header)

        # Initialize counter
        count = 0

        for index, row in df.iterrows():
            # Extract row data (handler-specific)
            row_data = handlers["row"](row)

            # Print progress message
            console.print(
                f"[magenta][{Utils.get_current_time()}][grey66] Processing "
                f"Row #: [dodger_blue1]{row_data['record']:04d}"
            )

            # Write KML body (handler-specific)
            kml_body = handlers["body"](row_data)
            f.write(kml_body)

            count += 1

        # Write closing block
        f.write(Utils.write_kml_closing())

    # Optionally write CSV
    if args.make_csv:
        df.to_csv(args.csv_file_path, index=False)

    # Time the script completed
    ending_time = time.perf_counter()

    # Total time
    total_time = ending_time - file_start_time

    # Write summary results to the screen
    Utils.end_program(
        query_command_string=query_command_string,
        start_time=args.start_time_apple,
        end_time=args.end_time_apple,
        csv_file=args.csv_file_path,
        count=count,
        kml_file=kml_file,
        total_time=total_time,
    )

    Utils.ask_open_kml_file(kml_file=kml_file)
