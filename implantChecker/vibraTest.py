#!/usr/bin/python
import sys
sys.path.append("../lib")
import lcd
import accelerometer
import math
import time

accel = accelerometer.mpu6050()
screen = lcd.lcd()

accel.setup()
accel.setSampleRate(100)
accel.setGResolution(16)
screen.lcd_clear()

I = accel.readData()

Threshold = 0.2
ShakeFlag = False

while True:
    while (accel.readStatus() & 1) == 0:
        pass
        I = accel.readData()
        PeakForce = 0
        for loop in range(20):
            while (accel.readStatus() & 1) == 0:
                pass
        C = accel.readData()
        CurrentForce = math.sqrt((C.Gx - I.Gx) * (C.Gx - I.Gx) +
                               (C.Gy - I.Gy) * (C.Gy - I.Gy) +
                               (C.Gz - I.Gz) * (C.Gz - I.Gz))
        if CurrentForce > PeakForce:
            PeakForce = CurrentForce
            StrPeak = str(PeakForce)
        if PeakForce > Threshold:
            if not(ShakeFlag):
                ShakeFlag = True
                screen.lcd_display_string(" Vibration Detected", 1)
                screen.lcd_display_string("Peak:" + StrPeak + "G", 2)
                time.sleep(3)
            else:
                ShakeFlag = False
        else:
            screen.lcd_display_string("    No Vibration   ", 1)