import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert

# ---- target_temperature: every branch + boundaries ----
def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_sleep_night_late():
    assert target_temperature("sleep", True, 23) == 18

def test_sleep_early_morning():
    assert target_temperature("sleep", True, 5) == 18      # hour < 6

def test_sleep_boundary_22():
    assert target_temperature("sleep", True, 22) == 18     # hour >= 22

def test_sleep_day():
    assert target_temperature("sleep", True, 12) == 20

def test_sleep_boundary_6():
    assert target_temperature("sleep", True, 6) == 20

def test_not_occupied():
    assert target_temperature("home", False, 12) == 18

def test_morning_start():
    assert target_temperature("home", True, 6) == 22

def test_morning_end_boundary():
    assert target_temperature("home", True, 9) == 20

def test_before_morning():
    assert target_temperature("home", True, 5) == 20

def test_evening_start():
    assert target_temperature("home", True, 17) == 21

def test_evening_end_boundary():
    assert target_temperature("home", True, 22) == 20

def test_default_daytime():
    assert target_temperature("home", True, 12) == 20

# ---- hvac_action: all branches ----
def test_idle_small_diff():
    assert hvac_action(20, 20.5, 10) == "idle"

def test_idle_negative_small_diff():
    assert hvac_action(20.5, 20, 10) == "idle"

def test_heat_boost():
    assert hvac_action(15, 20, 0) == "heat_boost"

def test_heat_normal():
    assert hvac_action(15, 20, 10) == "heat"

def test_heat_outside_boundary():
    assert hvac_action(15, 20, 5) == "heat"                # outside == 5, not < 5

def test_diff_exactly_one():
    assert hvac_action(19, 20, 10) == "heat"               # abs(diff) == 1, not idle

def test_cool_boost():
    assert hvac_action(25, 20, 35) == "cool_boost"

def test_cool_normal():
    assert hvac_action(25, 20, 20) == "cool"

def test_cool_outside_boundary():
    assert hvac_action(25, 20, 30) == "cool"               # outside == 30, not > 30

# ---- energy_alert: all branches ----
def test_no_readings():
    assert energy_alert([], 10) == "ok"

def test_all_under_limit():
    assert energy_alert([1, 2, 3], 10) == "ok"

def test_reading_equal_to_limit():
    assert energy_alert([10, 10], 10) == "ok"              # not strictly greater

def test_critical():
    assert energy_alert([10, 10, 1], 5) == "critical"

def test_exactly_half_is_warning():
    assert energy_alert([10, 1], 5) == "warning"           # over*2 == len, not >

def test_warning():
    assert energy_alert([10, 1, 1, 1], 5) == "warning"