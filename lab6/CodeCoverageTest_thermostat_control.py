import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert

# ---- target_temperature ----
def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_sleep_night():
    assert target_temperature("sleep", True, 23) == 18

def test_sleep_day():
    assert target_temperature("sleep", True, 12) == 20

def test_not_occupied():
    assert target_temperature("home", False, 12) == 18

def test_morning():
    assert target_temperature("home", True, 7) == 22

def test_evening():
    assert target_temperature("home", True, 18) == 21

def test_default_daytime():
    assert target_temperature("home", True, 12) == 20

# ---- hvac_action ----
def test_idle():
    assert hvac_action(20, 20.5, 10) == "idle"

def test_heat():
    assert hvac_action(15, 20, 10) == "heat"

def test_cool():
    assert hvac_action(25, 20, 20) == "cool"

# ---- energy_alert ----
def test_no_readings():
    assert energy_alert([], 10) == "ok"

def test_critical():
    assert energy_alert([10, 10, 1], 5) == "critical"

def test_warning():
    assert energy_alert([10, 1, 1, 1], 5) == "warning"