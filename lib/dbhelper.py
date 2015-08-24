# -*- coding: utf-8 -*-
import MySQLdb



class dbHelper:

    def __init__(self):
        db = MySQLdb.connect("192.168.2.3", "fft", "password", "fft")
        cursor = db.cursor()
