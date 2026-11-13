import math
import re
from statistics import mean


def parse_setpoint(text):
    """Convert a valid C/F setpoint to Celsius; otherwise return None."""
    if not isinstance(text, str):
        return None

    text = text.strip()

    if len(text) < 2:
        return None

    unit = text[-1].upper()
    if unit not in ("C", "F"):
        return None

    try:
        value = float(text[:-1].strip())
    except (ValueError, OverflowError):
        return None

    if not math.isfinite(value):
        return None

    if unit == "F":
        # Divide first to reduce the risk of intermediate overflow.
        value = (value - 32) / 9 * 5

    if not math.isfinite(value):
        return None

    return round(value, 1)


def average_temperature(readings_csv):
    """Average finite CSV readings; return None for invalid input."""
    if not isinstance(readings_csv, str):
        return None

    parts = readings_csv.split(",")

    # Reject empty input, trailing commas, and missing readings.
    if any(not part.strip() for part in parts):
        return None

    try:
        values = [float(part.strip()) for part in parts]
    except (ValueError, OverflowError):
        return None

    if not all(math.isfinite(value) for value in values):
        return None

    # statistics.mean avoids overflowing a naive floating-point sum.
    result = mean(values)
    return result if math.isfinite(result) else None


def schedule_slot(time_text):
    """Classify a valid HH:MM time; otherwise return None."""
    if not isinstance(time_text, str):
        return None

    time_text = time_text.strip()

    if re.fullmatch(r"[0-9]{2}:[0-9]{2}", time_text) is None:
        return None

    hour, minute = map(int, time_text.split(":"))

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None

    # Preserve the original output format for valid times.
    if hour < 6:
        return "night " + time_text.split(":")[1]

    return "day " + str(minute)


def main():
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    result = parse_setpoint(user_input)

    if result is None:
        print("Invalid setpoint. Enter a finite number followed by C or F.")
    else:
        print("Setpoint in Celsius:", result)

    print("\n==== Running average_temperature ====")
    user_input = input(
        "Enter sensor readings as CSV (e.g. 20.5,21,22.5): "
    )
    result = average_temperature(user_input)

    if result is None:
        print("Invalid readings. Enter finite numbers separated by commas.")
    else:
        print("Average Temperature:", result)

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    result = schedule_slot(user_input)

    if result is None:
        print("Invalid time. Use HH:MM between 00:00 and 23:59.")
    else:
        print("Schedule Slot:", result)


if __name__ == "__main__":
    main()