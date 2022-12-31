from homeassistant.const import TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.util.unit_conversion import TemperatureConverter
import logging


def simple_celsius_to_fahrenheit(temp: float) -> float:
    return temp * 9 / 5 + 32


def convert_temp(hass, node_units, temp):
    # Temperatures are converted to the units of the HA
    # instance, so do the same for comparison
    unit = TEMP_CELSIUS if node_units == "C" else TEMP_FAHRENHEIT
    return TemperatureConverter.convert(temp, unit, hass.config.units.temperature_unit)


def round_temp(hass, temp):
    print(f"TEMP {temp} {type(temp)}")
    # HA uses different precisions for Fahrenheit (whole
    # integers) vs Celsius (tenths)
    if hass.config.units.temperature_unit == TEMP_CELSIUS:
        return round(temp, 1)
    else:
        return round(temp)


def assert_log_message(
    caplog, name: str, levelno: int, message: str, phase="call"
) -> None:
    def _find_message(r: logging.LogRecord) -> bool:
        return r.name == name and r.levelno == levelno and r.message == message

    assert any(
        # Ignoring typing due to https://github.com/python/mypy/issues/12682
        filter(_find_message, caplog.get_records(phase))  # type: ignore
    )


def assert_no_log_errors(caplog, phase="call") -> None:
    errors = [
        record
        for record in caplog.get_records("call")
        if record.levelno >= logging.ERROR
    ]
    assert not errors
