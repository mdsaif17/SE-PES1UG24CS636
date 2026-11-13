import math

from hypothesis import given, strategies as st

from thermostat_control import (
    parse_setpoint,
    average_temperature,
    schedule_slot,
)


# Chosen validation policy:
# Invalid inputs should return None without crashing.
# Valid inputs should produce the expected result.


@given(st.text() | st.none())
def test_parse_setpoint_no_crash(s):
    result = parse_setpoint(s)
    assert result is None or (
        isinstance(result, (int, float)) and math.isfinite(result)
    )


@given(st.text() | st.none())
def test_average_temperature_no_crash(s):
    result = average_temperature(s)
    assert result is None or (
        isinstance(result, (int, float)) and math.isfinite(result)
    )


@given(st.text() | st.none())
def test_schedule_slot_no_crash(s):
    result = schedule_slot(s)
    if result is not None:
        label, minute = result.split()
        assert label in ("night", "day")
        assert 0 <= int(minute) <= 59


@given(st.integers(min_value=-1000, max_value=1000))
def test_celsius_setpoint(value):
    assert parse_setpoint(f"{value}C") == round(float(value), 1)


@given(st.integers(min_value=-1000, max_value=1000))
def test_fahrenheit_setpoint(value):
    expected = round((value - 32) * 5 / 9, 1)
    assert parse_setpoint(f"{value}F") == expected


@given(
    st.lists(
        st.integers(min_value=-1000, max_value=1000),
        min_size=1,
        max_size=50,
    )
)
def test_average_valid_readings(values):
    csv = ",".join(str(value) for value in values)
    expected = sum(values) / len(values)
    assert math.isclose(
        average_temperature(csv),
        expected,
        rel_tol=1e-9,
        abs_tol=1e-9,
    )


@given(
    hour=st.integers(min_value=0, max_value=23),
    minute=st.integers(min_value=0, max_value=59),
)
def test_valid_schedule(hour, minute):
    result = schedule_slot(f"{hour:02d}:{minute:02d}")
    label, returned_minute = result.split()
    assert label == ("night" if hour < 6 else "day")
    assert int(returned_minute) == minute


@given(st.sampled_from([
    "", "21", "21K", "abcC", "NaNC", "infF", None,
]))
def test_invalid_setpoints(s):
    assert parse_setpoint(s) is None


@given(st.sampled_from([
    "", ",", "20,,21", "abc,21", "NaN,20", "inf,20", None,
]))
def test_invalid_readings(s):
    assert average_temperature(s) is None


@given(st.sampled_from([
    "", "24:00", "-1:30", "12:60", "12:-1",
    "ab:cd", "12", "12:30:45", None,
]))
def test_invalid_schedule(s):
    assert schedule_slot(s) is None