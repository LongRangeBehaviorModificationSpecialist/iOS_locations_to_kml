# !/usr/bin/env python3

"""Shared data models for the cache conversion tool."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from rich.traceback import install


install(show_locals=True)


@dataclass(frozen=True)
class ConversionArgs:
    """
    Arguments shared across all database conversion functions.

    Attributes:
        python_file: Path to the source Python script being processed
        source: Input source path/database location
        dest: Output destination directory
        make_csv: Whether to export additional CSV output alongside KML
        start_time: Start timestamp for time-range filtering (original string)
        end_time: (Required) End timestamp for time-range filtering (original
            string)
        file_time: Timestamp to apply to output file metadata
        db_type: Database type identifier ("1" through "6")
        tz_code: Timezone code (e.g., "UTC", "America/New_York")
        start_time_apple: Converted Apple Absolute Time for start (float
            seconds)
        end_time_apple: (Required) Converted Apple Absolute Time for end
            (float seconds)
        base_filename: Base name for output files (default: "results")
        run_timestamp: Captured timestamp at startup for consistent naming
    """
    python_file: str
    source: str
    dest: str
    make_csv: bool
    start_time: str
    end_time: str
    # file_time: str
    tz_code: str
    db_type: str

    # Apple Absolute Time values (converted in make_klm_cli.py)
    start_time_apple: float = 0.0
    end_time_apple: float = 0.0

    # Optional customization
    base_name: str = "results"
    run_timestamp: str = ""

    def __post_init__(self) -> None:
        """Validate arguments after initialization.

        Checks:
            1. end_time is always required (SQL needs it for WHERE BETWEEN
                filter)
            2. If start_time is provided, it must be before end_time
            3. Source file exists
            4. Destination directory is writable
            5. db_type is supported (1-6)
        """

        # --- Time Validation ---
        # End time value is always required (SQL uses BETWEEN filter)
        if self.end_time_apple == 0.0:
            raise ValueError(
                "An end time value is required to perform the SQL query"
            )

        # If start_time is provided, validate it's before end_time
        if self.start_time_apple != 0.0:
            if self.start_time_apple >= self.end_time_apple:
                raise ValueError(
                    f"start_time value ({self.start_time}) must be before "
                    f"end_time value ({self.end_time}). Got {self.start_time} "
                    f" →  {self.end_time}"
                )

        # --- Source File Validation ---
        if not Path(self.source).exists():
            raise FileNotFoundError(f"Source file not found → {self.source}")

        # --- Destination Directory Validation ---
        try:
            Path(self.dest).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"Cannot write to destination → {self.dest}")
        except OSError as e:
            raise OSError(
                f"Invalid destination directory: '{self.dest}' → {e}"
            )

        # --- db_type Validation ---
        if self.db_type not in ("1", "2", "3", "4", "5", "6"):
            raise ValueError(
                f"Unsupported db_type: '{self.db_type}'. "
                f"The value must be one of: 1, 2, 3, 4, 5, 6"
            )

    @property
    def source_path(self) -> Path:
        """Return source as Path object for convenient file operations."""
        return Path(self.source)

    @property
    def dest_path(self) -> Path:
        """Return destination directory as Path object."""
        return Path(self.dest)

    @property
    def timestamp(self) -> str:
        """Return timestamp (use captured value or generate fresh)."""
        return self.run_timestamp or datetime.now().strftime("%Y-%m-%d_%H%M%S")

    @property
    def base_filename(self) -> str:
        """Generate base filename WITHOUT extension."""
        return f"{self.timestamp}_{self.base_name}"

    @property
    def kml_filename(self) -> str:
        """KML output filename with extension."""
        return f"{self.base_filename}.kml"

    @property
    def csv_filename(self) -> str:
        """CSV output filename with extension."""
        return f"{self.base_filename}.csv"

    @property
    def kml_file_path(self) -> Path:
        """Full path to KML output file."""
        return Path(self.dest) / self.kml_filename

    @property
    def csv_file_path(self) -> Path:
        """Full path to CSV output file (same as KML but .csv extension)."""
        return Path(self.dest) / self.csv_filename

    @property
    def time_range_description(self) -> str:
        """Human-readable description of the time range."""
        if self.has_time_filter:
            return f"{self.start_time} to {self.end_time}"
        else:
            return f"From beginning until {self.end_time}"

    @property
    def has_time_filter(self) -> bool:
        """True if both start and end times were provided."""
        return bool(
            self.start_time and self.end_time and
            self.start_time_apple > 0 and self.end_time_apple > 0
        )

    def to_dict(self) -> dict:
        """Convert to dictionary (useful for logging/serialization)."""
        import dataclasses
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        """Readable string representation for debugging/logging."""
        return (
            f"ConversionArgs( "
            f"source={self.source}, "
            f"dest={self.dest}, "
            f"db_type={self.db_type}, "
            f"make_csv={self.make_csv}, "
            f"time_range={self.time_range_description}, "
            f"start_time_apple={self.start_time_apple}, "
            f"end_time_apple={self.end_time_apple}, "
            f"time_zone={self.tz_code} "
            f")"
        )
