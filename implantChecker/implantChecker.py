#!/usr/bin/python
import sys
sys.path.append("../lib")
import lcd
import math
import time
import numpy
import accelerometer
import dbhelper
from scipy.fftpack import fft
from scipy.signal import hanning
from scipy.signal import hamming

TargetSampleNumber = 1024
TargetRate = float(125)
Email = "raditiya@me.com"
DataID = "RADIT0001"

screen = lcd.lcd()
accel = accelerometer.mpu6050()
mdb = dbhelper.dbHelper()

screen.lcd_clear()
accel.setup()
accel.setGResolution(2)
accel.setSampleRate(TargetRate)
accel.enableFifo(False)
time.sleep(0.01)

print "Capture {0} samples at {1} samples/sec".format(TargetSampleNumber, accel.SampleRate)
screen.lcd_display_string("Capture {0} samples".format(TargetSampleNumber), 1)
screen.lcd_display_string("at {0} samples/sec".format(accel.SampleRate), 2)
screen.lcd_display_string("Press enter to start", 3)
raw_input("Press enter to start")
screen.lcd_clear()

accel.resetFifo()
accel.enableFifo(True)
time.sleep(0.01)

Values = []
Total = 0

while True:
    if accel.fifoCount == 0:
        Status = accel.readStatus()
        if (Status & 0x10) == 0x10:
            print "Overrun Error! Quitting.\n"
            quit()
        if (Status & 0x01) == 0x01:
            Values.extend(accel.readDataFromFifo())
    else:
        Values.extend(accel.readDataFromFifo())

    Total = len(Values) / 14

    if Total >= TargetSampleNumber:
        break

if Total > 0:
    Status = accel.readStatus()
    if (Status & 0x10) == 0x10:
        print "Overrun Error! Quitting.\n"
        quit()

    print "Inserting raw into Database"
    screen.lcd_display_string("Insert into Database.", 1)
    mdb.insertData(Values, TargetSampleNumber, Email, DataID)
    fftdata = []
    for loop in range(TargetSampleNumber):
        SimpleSample = Values[loop * 14: loop * 14 + 14]
        I = accel.convertData(SimpleSample)
        CurrentForce = math.sqrt((I.Gx * I.Gx) + (I.Gy * I.Gy) + (I.Gz * I.Gz))
        fftdata.append(CurrentForce)

    print "Calculate FFT"
    screen.lcd_display_string("  Calculating FFT  ",2)
    hanWindow = hanning(TargetSampleNumber)
    hammWindow = hamming(TargetSampleNumber)
    fourier = fft(fftdata)
    fftData = numpy.abs(fourier[0: len(fourier) / 2 + 1]) / TargetSampleNumber

    print "Inserting FFT Result to Database"
    screen.lcd_display_string("Recording FFT Results", 3)
    mdb.insertFFT(fftData, TargetSampleNumber, TargetRate, Email, DataID)
    frequency = []
    Peak = 0
    PeakIndex = 0
    for loop in range(TargetSampleNumber / 2 + 1):
        frequency.append(loop * TargetRate / TargetSampleNumber)
        if loop > 0:
            if fftData[loop] > Peak:
                Peak = fftData[loop]
                PeakIndex = loop
    print "Peak at {0}Hz = {1}".format(frequency[PeakIndex], Peak)
    screen.lcd_clear()
    screen.lcd_display_string("-------Peak at-------",1)
    screen.lcd_display_string("{0}Hz".format(frequency[PeakIndex]), 2)
    screen.lcd_display_string("          =          ",3)
    screen.lcd_display_string(str(Peak), 4)
print "Done!"
