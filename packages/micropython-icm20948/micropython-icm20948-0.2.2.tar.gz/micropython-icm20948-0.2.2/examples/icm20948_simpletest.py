# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
from micropython_icm20948 import icm20948

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
icm = icm20948.ICM20948(i2c)


while True:
    accx, accy, accz = icm.acceleration
    gyrox, gyroy, gyroz = icm.gyro
    print(f"x: {accx}m/s2, y: {accy},m/s2 z: {accz}m/s2")
    print(f"x: {gyrox}°/s, y: {gyroy}°/s, z: {gyroz}°/s")
    time.sleep(1)
