# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mmc5983 import mmc5983

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mmc = mmc5983.MMC5983(i2c)

mmc.bandwidth = mmc5983.BW_400HZ

while True:
    for bandwidth in mmc5983.bandwidth_values:
        print("Current Bandwidth setting: ", mmc.bandwidth)
        for _ in range(10):
            magx, magy, magz = mmc.magnetic
            print(f"X: {magx:.2f}uT, Y: {magy:.2f}uT, Z: {magz:.2f}uT")
            print()
            time.sleep(0.5)
        mmc.bandwidth = bandwidth
