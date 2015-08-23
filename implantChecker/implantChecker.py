#!/usr/bin/python
import sys
sys.path.append("../lib")
import lcd
import math
import time
import numpy
import accelerometer
from scipy.fftpack import fft
from scipy.signal import hanning
from scipy.signal import hamming
from time import *

TargetSampleNumber = 1024
TargetRate = 125

screen = lcd.lcd()
accel = accelerometer.mpu6050()

screen.lcd_clear()
accel.setup()
accel.setGResolution(2)
accel.setSampleRate(TargetRate)
accel.enableFifo(False)
time.sleep(0.01)

print "Capturing {0} samples at {1} samples/sec".format(TargetSampleNumber, mpu6050.SampleRate)

raw_input("Press enter to start")

accel.resetFifo()
accel.enableFifo(True)
time.sleep(0.01)

Values = []
Total = 0
