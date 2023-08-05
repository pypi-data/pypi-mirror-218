# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`mmc5983`
================================================================================

MicroPython Library for the Memsic MMC5983 Magnetometer


* Author(s): Jose D. Montoya


"""
import time
from micropython import const
from micropython_mmc5983.i2c_helpers import CBits, RegisterStruct

try:
    from typing import Tuple
except ImportError:
    pass


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_MMC5983.git"

_REG_WHOAMI = const(0x2F)
_DATA = const(0x00)
_INTERNAL_CONTROL0 = const(0x09)
_INTERNAL_CONTROL1 = const(0x0A)
_INTERNAL_CONTROL2 = const(0x0B)

ONE_SHOT = const(0b0)
CONTINUOUS = const(0b1)
operation_mode_values = (ONE_SHOT, CONTINUOUS)

SCALE_FACTOR = const(16384)

CM_OFF = const(0b000)
CM_1HZ = const(0b001)
CM_10HZ = const(0b010)
CM_20HZ = const(0b011)
CM_50HZ = const(0b100)
CM_100HZ = const(0b101)
CM_200HZ = const(0b110)
CM_1000HZ = const(0b111)
continuous_mode_frequency_values = (
    CM_OFF,
    CM_1HZ,
    CM_10HZ,
    CM_20HZ,
    CM_50HZ,
    CM_100HZ,
    CM_200HZ,
    CM_1000HZ,
)

BW_100HZ = const(0b00)
BW_200HZ = const(0b01)
BW_400HZ = const(0b10)
BW_800HZ = const(0b11)
bandwidth_values = (BW_100HZ, BW_200HZ, BW_400HZ, BW_800HZ)
delay_times = (0.008, 0.004, 0.002, 0.00005)


class MMC5983:
    """Driver for the MMC5983 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the MMC5983 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x30`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`MMC5983` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_mmc5983 import mmc5983

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        mmc5983 = mmc5983.MMC5983(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _device_id = RegisterStruct(_REG_WHOAMI, "B")
    _raw_data = RegisterStruct(_DATA, "HHHB")
    _temperature = RegisterStruct(0x07, "B")

    _bandwidth = CBits(2, _INTERNAL_CONTROL1, 0)

    _continuous_mode_frequency = CBits(3, _INTERNAL_CONTROL2, 0)
    _operation_mode = CBits(1, _INTERNAL_CONTROL2, 3)

    _start_magnetic_measure = CBits(1, _INTERNAL_CONTROL0, 0)
    _start_temperature_measure = CBits(1, _INTERNAL_CONTROL0, 1)

    def __init__(self, i2c, address: int = 0x30) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0x30:
            raise RuntimeError("Failed to find MMC5983")

        self.operation_mode = CONTINUOUS
        self.continuous_mode_frequency = CM_1HZ
        self.bandwidth = BW_100HZ

    @property
    def operation_mode(self) -> str:
        """
        Sensor operation_mode. In order to enter the continuous mode,
        :attr:`continuous_mode_frequency` cannot be :attr:`CM_OFF`

        +--------------------------------+-----------------+
        | Mode                           | Value           |
        +================================+=================+
        | :py:const:`mmc5983.ONE_SHOT`   | :py:const:`0b0` |
        +--------------------------------+-----------------+
        | :py:const:`mmc5983.CONTINUOUS` | :py:const:`0b1` |
        +--------------------------------+-----------------+
        """
        values = ("ONE_SHOT", "CONTINUOUS")
        return values[self._om_cached]

    @operation_mode.setter
    def operation_mode(self, value: int) -> None:
        if value not in operation_mode_values:
            raise ValueError("Value must be a valid operation_mode setting")
        if self._continuous_mode_frequency == 0:
            raise ValueError("Please select first a valid continuous mode frequency")
        self._operation_mode = value
        self._om_cached = value

    @property
    def continuous_mode_frequency(self) -> str:
        """
        Sensor continuous_mode_frequency determine how often the chip
        will take measurements in Continuous Measurement Mode. The frequency is
        based on the assumption that :attr:`bandwidth` is :attr:`BW_100HZ`

        +-------------------------------+-------------------+
        | Mode                          | Value             |
        +===============================+===================+
        | :py:const:`mmc5983.CM_OFF`    | :py:const:`0b000` |
        +-------------------------------+-------------------+
        | :py:const:`mmc5983.CM_1HZ`    | :py:const:`0b001` |
        +-------------------------------+-------------------+
        | :py:const:`mmc5983.CM_10HZ`   | :py:const:`0b010` |
        +-------------------------------+-------------------+
        | :py:const:`mmc5983.CM_20HZ`   | :py:const:`0b011` |
        +-------------------------------+-------------------+
        | :py:const:`mmc5983.CM_50HZ`   | :py:const:`0b100` |
        +-------------------------------+-------------------+
        | :py:const:`mmc5983.CM_100HZ`  | :py:const:`0b101` |
        +-------------------------------+-------------------+
        | :py:const:`mmc5983.CM_200HZ`  | :py:const:`0b110` |
        +-------------------------------+-------------------+
        | :py:const:`mmc5983.CM_1000HZ` | :py:const:`0b111` |
        +-------------------------------+-------------------+
        """
        values = (
            "CM_OFF",
            "CM_1HZ",
            "CM_10HZ",
            "CM_20HZ",
            "CM_50HZ",
            "CM_100HZ",
            "CM_200HZ",
            "CM_1000HZ",
        )
        return values[self._cmfc]

    @continuous_mode_frequency.setter
    def continuous_mode_frequency(self, value: int) -> None:
        if value not in continuous_mode_frequency_values:
            raise ValueError("Value must be a valid continuous_mode_frequency setting")
        if value == CM_200HZ and self._bandwidth < BW_200HZ:
            raise ValueError("Please set a correct bandwidth value for this setting")
        if value == CM_1000HZ and self._bandwidth < BW_800HZ:
            raise ValueError("Please set a correct bandwidth value for this setting")

        self.operation_mode = ONE_SHOT
        self._continuous_mode_frequency = value
        self._cmfc = value
        self.operation_mode = CONTINUOUS

    @property
    def bandwidth(self) -> str:
        """
        Sensor bandwidth. These bandwidth selection bits adjust the length
        of the decimation filter. They control the duration of each measurement

        .. Note:

            X/Y/Z channel measurements are taken in parallel.


        +------------------------------+------------------+
        | Mode                         | Value            |
        +==============================+==================+
        | :py:const:`mmc5983.BW_100HZ` | :py:const:`0b00` |
        +------------------------------+------------------+
        | :py:const:`mmc5983.BW_200HZ` | :py:const:`0b01` |
        +------------------------------+------------------+
        | :py:const:`mmc5983.BW_400HZ` | :py:const:`0b10` |
        +------------------------------+------------------+
        | :py:const:`mmc5983.BW_800HZ` | :py:const:`0b11` |
        +------------------------------+------------------+
        """
        values = ("BW_100HZ", "BW_200HZ", "BW_400HZ", "BW_800HZ")
        return values[self._bw_cached]

    @bandwidth.setter
    def bandwidth(self, value: int) -> None:
        if value not in bandwidth_values:
            raise ValueError("Value must be a valid bandwidth setting")
        self.operation_mode = ONE_SHOT
        self._bandwidth = value
        self._bw_cached = value
        self.operation_mode = CONTINUOUS

    @property
    def magnetic(self) -> Tuple[float, float, float]:
        """
        Returns magnetic data in uT
        """

        x, y, z, extra = self._raw_data
        time.sleep(0.2)
        x_raw = (x << 2) | (((extra & 0xC0) >> 6) & 0x3)
        y_raw = (y << 2) | (((extra & 0x30) >> 4) & 0x3)
        z_raw = (z << 2) | (((extra & 0x03) >> 2) & 0x3)

        # https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/
        x_scale = x_raw - 131072.0
        x_scale = (x_scale / 131072.0) * 100

        y_scale = y_raw - 131072.0
        y_scale = (y_scale / 131072.0) * 100

        z_scale = z_raw - 131072.0
        z_scale = (z_scale / 131072.0) * 100

        return x_scale, y_scale, z_scale

    @property
    def temperature(self) -> float:
        """
        Returns Temperature in Celsius
        """
        self.operation_mode = ONE_SHOT
        self._start_temperature_measure = True

        t_raw = self._temperature
        self.operation_mode = CONTINUOUS

        return t_raw * 200.0 / 256.0 - 75.0
