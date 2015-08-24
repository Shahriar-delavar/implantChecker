# -*- coding: utf-8 -*-
import MySQLdb as mdb
import struct
import math


class accelData:

    def __init__(self):
        self.Gx = 0
        self.Gy = 0
        self.Gz = 0
        self.Temp = 0
        self.Gyrox = 0
        self.Gyroy = 0
        self.Gyroz = 0


class dbHelper:

    AccelerationFactor = 2.0 / 32768.0
    GyroFactor = 500.0 / 32768.0
    TemperatureGain = 1.0 / 340.0
    TemperatureOffset = 36.53

    def __init__(self):
        self.db = mdb.connect("127.0.0.1", "fft", "password", "fft")

    def convertData(self, ListData):
        ShortData = struct.unpack(">hhhhhhh", buffer(bytearray(ListData)))
        AccData = accelData()
        AccData.Gx = ShortData[0] * self.AccelerationFactor
        AccData.Gy = ShortData[1] * self.AccelerationFactor
        AccData.Gz = ShortData[2] * self.AccelerationFactor
        AccData.Temperature = ShortData[3] * self.TemperatureGain + self.TemperatureOffset
        AccData.Gyrox = ShortData[4] * self.GyroFactor
        AccData.Gyroy = ShortData[5] * self.GyroFactor
        AccData.Gyroz = ShortData[6] * self.GyroFactor
        return AccData

    def insertData(self, Data, SampleNumber, DataID):
        with self.db:
            cur = self.db.cursor()
            for loop in range(SampleNumber):
                SimpleSample = Data[loop * 14: loop * 14 + 14]
                I = self.convertData(SimpleSample)
                CurrentForce = math.sqrt((I.Gx * I.Gx) + (I.Gy * I.Gy) + (I.Gz * I.Gz))
                cur.execute("INSERT INTO tb_data(data_gx, data_gy, data_gz, data_force, serial_id) VALUES(%s, %s, %s, %s, %s)",
                    (I.Gx, I.Gy, I.Gz, CurrentForce, DataID))

    def insertFFT(self, Data, SampleNumber, TargetRate, DataID):
        frequency = []
        with self.db:
            cur = self.db.cursor()
            for loop in range(SampleNumber / 2 + 1):
                frequency.append(loop * TargetRate / SampleNumber)
                if(frequency[loop] != 0):
                    cur.execute("INSERT INTO tb_fft(fft_frequency, fft_data, serial_id) VALUES(%s, %s, %s)",
                    (frequency[loop], Data[loop], DataID))

    def getUserID(self, Email):
        with self.db:
            cur = self.db.cursor()
            cur.execute("SELECT user_id FROM tb_users WHERE user_email= %s", (Email))
            row = cur.fetchone()
            if row:
                emailID = row[0]
            else:
                emailID = ""
        return emailID

    def addSerial(self, Serial, Email):
        userID = self.getUserID(Email)
        with self.db:
            cur = self.db.cursor()
            cur.execute("INSERT INTO tb_serial(user_id, serial_name) VALUES(%s, %s)",
            (userID, Serial))

    def getSerialID(self, Serial):
        with self.db:
            cur = self.db.cursor()
            cur.execute("SELECT serial_id FROM tb_serial WHERE serial_name= %s", (Serial))
            row = cur.fetchone()
            if row:
                serialID = row[0]
            else:
                serialID = ""
        return serialID
