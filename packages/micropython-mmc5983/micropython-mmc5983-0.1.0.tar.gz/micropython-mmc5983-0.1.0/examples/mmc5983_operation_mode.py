# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mmc5983 import mmc5983

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mmc = mmc5983.MMC5983(i2c)

mmc.operation_mode = mmc5983.CONTINUOUS

while True:
    for operation_mode in mmc5983.operation_mode_values:
        print("Current Operation mode setting: ", mmc.operation_mode)
        for _ in range(10):
            magx, magy, magz = mmc.magnetic
            print(f"X: {magx:.2f}uT, Y: {magy:.2f}uT, Z: {magz:.2f}uT")
            print()
            time.sleep(0.5)
        mmc.operation_mode = operation_mode
