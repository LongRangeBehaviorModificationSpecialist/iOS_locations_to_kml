EXISTING_DATABASES = {
    "Cache.sqlite",
    "cache_encryptedB.db",
    "Cloud-V2.sqlite",
    "Local.sqlite",
}

DATABASE_IDS = {
    "1": "Cache.sqlite (Location History)",
    "2": "cache_encryptedB.db (WiFi locations)",
    "3": "cache_encryptedB.db (LTE locations)",
    "4": "Cloud-V2.sqlite (Significant Locations)",
    "5": "Local.sqlite (Significant Location Visits)",
    "6": "Local.sqlite (Vehicle Locations)",
}


US_TIME_ZONES = {
    # Eastern Time
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "ET":  "America/New_York",

    # Central Time
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "CT":  "America/Chicago",

    # Mountain Time
    "MST": "America/Denver",
    "MDT": "America/Denver",
    "MT":  "America/Denver",

    # Mountain Time (Arizona - No DST)
    "AZ":  "America/Phoenix",

    # Pacific Time
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "PT":  "America/Los_Angeles",

    # Alaska & Hawaii
    "AKT": "America/Anchorage",
    "HST": "Pacific/Honolulu",
    "HT":  "Pacific/Honolulu",

    # UTC/GMT Reference
    "UTC": "UTC",
    "GMT": "GMT"
}
