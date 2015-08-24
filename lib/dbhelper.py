# -*- coding: utf-8 -*-
import MySQLdb as mdb
import struct


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
        self.db = mdb.connect("localhost", "fft", "password", "fft")

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

    def insertData(self, Data, SampleNumber, Email, DataID):
        userID = self.getUserID(Email)

        with self.db:
            cur = self.db.cursor()
            for loop in range(SampleNumber):
                SimpleSample = Data[loop * 14: loop * 14 + 14]
                I = self.convertData(SimpleSample)
                cur.execute("INSERT INTO tb_data values('', %s, %s, %s, %s, %s)",
                    (userID, I.Gx, I.Gy, I.Gz, DataID))

    def getUserID(self, Email):
        with self.db:
            cur = self.db.cursor()
            cur.execute("SELECT user_id FROM tb_users where user_email= %s", (Email))
            row = cur.fetchone()
            emailID = row[0]
        return emailID