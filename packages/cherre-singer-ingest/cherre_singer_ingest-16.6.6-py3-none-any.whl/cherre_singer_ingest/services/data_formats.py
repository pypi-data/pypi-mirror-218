def iso8601_timestamp_to_avro_fixed_precision(iso8601_timestamp: str):
    """
    Takes a ISO 8601 formatted timestamp and ensures it has a fixed subsecond
    precision, with three decimal places, required by AVRO tooling.
    """
    timestamp, tz = iso8601_timestamp.split("+")
    # Check that timestamp has subseconds. If the timestamp has no subseconds, the part after . will not exist
    if len(timestamp.split(".")) > 1:
        datetime, subseconds = timestamp.split(".")
    else:
        datetime = timestamp.split(".")[0]
        subseconds = "000"
    return datetime + "." + subseconds.ljust(3, "0") + "+" + tz
