# SPDX-FileCopyrightText: Copyright (c) 2023 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_ad5245`
================================================================================

A CircuitPython driver for the AD5245 digital potentiometer.
Thank you to Bryan Siepert for the driver concept inspiration.

* Author(s): JG

Implementation Notes
--------------------

**Hardware:**

* Cedar Grove Studios AD5245 breakout or equivalent

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_AD5245.git"


_AD5245_DEFAULT_ADDRESS = 0x2C  # 44, 0b00101100


class AD5245:
    """Class representing the Cedar Grove AD5245, an I2C digital linear taper
    potentiometer.

    :param address: The I2C device address for the device. Default is ``0x2C``.
    :param wiper: The initial wiper value. Default is 0."""

    _BUFFER = bytearray(1)

    def __init__(self, address=_AD5245_DEFAULT_ADDRESS, wiper=0):
        self._i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
        self._device = I2CDevice(self._i2c, address)

        self._wiper = wiper
        self._default_wiper = wiper
        self._normalized_wiper = self._wiper / 255.0
        self._write_to_device(0, wiper)

    def _write_to_device(self, command, value):
        """Write command and data value to the device."""
        with self._device:
            self._device.write(bytes([command & 0xFF, value & 0xFF]))

    def _read_from_device(self):
        """Reads the contents of the data register."""
        with self._device:
            self._device.readinto(self._BUFFER)
        return self._BUFFER

    @property
    def wiper(self):
        """The raw value of the potentiometer's wiper."""
        return self._wiper

    @wiper.setter
    def wiper(self, value=0):
        """Set the raw value of the potentiometer's wiper.
        :param value: The raw wiper value from 0 to 255."""
        if value < 0 or value > 255:
            raise ValueError("raw wiper value must be from 0 to 255")
        self._write_to_device(0x00, value)
        self._wiper = value

    @property
    def normalized_wiper(self):
        """The normalized value of the potentiometer's wiper."""
        return self._normalized_wiper

    @normalized_wiper.setter
    def normalized_wiper(self, value):
        """Set the normalized value of the potentiometer's wiper.
        :param value: The normalized wiper value from 0.0 to 1.0."""
        if value < 0 or value > 1.0:
            raise ValueError("normalized wiper value must be from 0.0 to 1.0")
        self._write_to_device(0x00, int(value * 255.0))
        self._normalized_wiper = value

    @property
    def default_wiper(self):
        """The default value of the potentiometer's wiper."""
        return self._default_wiper

    @default_wiper.setter
    def default_wiper(self, value):
        """Set the default value of the potentiometer's wiper.
        :param value: The raw wiper value from 0 to 255."""
        if value < 0 or value > 255:
            raise ValueError("default wiper value must be from 0 to 255")
        self._default_wiper = value

    def set_default(self, default):
        """A dummy helper to maintain UI compatibility digital
        potentiometers with EEROM capability (dS3502). The AD5245's
        wiper value will be set to 0 unless the default value is
        set explicitly during or after class instantiation."""
        self._default_wiper = default

    def shutdown(self):
        """Connects the W to the B terminal and opens the A terminal connection.
        The contents of the wiper register are not changed."""
        self._write_to_device(0x20, 0)
