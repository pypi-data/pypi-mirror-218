# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mmc5983 import mmc5983

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mmc = mmc5983.MMC5983(i2c)

mmc.continuous_mode_frequency = mmc5983.CM_20HZ

while True:
    for continuous_mode_frequency in mmc5983.continuous_mode_frequency_values:
        print(
            "Current Continuous mode frequency setting: ", mmc.continuous_mode_frequency
        )
        for _ in range(5):
            magx, magy, magz = mmc.magnetic
            print(f"X: {magx:.2f}uT, Y: {magy:.2f}uT, Z: {magz:.2f}uT")
            time.sleep(0.5)
        mmc.continuous_mode_frequency = continuous_mode_frequency
