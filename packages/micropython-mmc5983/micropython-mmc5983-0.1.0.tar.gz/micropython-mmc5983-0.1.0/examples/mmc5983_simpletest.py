# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mmc5983 import MMC5983

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mmc = MMC5983(i2c)

while True:
    magx, magy, magz = mmc.magnetic
    print(f"X: {magx:.2f}uT, Y: {magy:.2f}uT, Z: {magz:.2f}uT")
    time.sleep(0.5)
    temp = mmc.temperature
    print(f"Temperature {temp:.1f}C")
    print()
    time.sleep(0.5)
