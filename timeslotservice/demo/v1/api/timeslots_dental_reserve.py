# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import sqlite3


class TimeslotsDentalReserve(Resource):
    def insert_record(self, db_name, client_name, dentist_name, time):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        appointment = False
        # create dental_booking if not exist
        c.execute(''' CREATE TABLE IF NOT EXISTS DENTAL_BOOKING 
                    (booking_id integer PRIMARY KEY AUTOINCREMENT,
                    client_name text NOT NULL,
                    dentist_name text NOT NULL,
                    time integer NOT NULL,
                    status text NOT NULL); ''')

        # check whether an appointment is exist, avoid multiple booking
        c.execute(f"SELECT status FROM DENTAL_TIMESLOTS WHERE dentist_name = '{dentist_name}' AND time = {time};")
        r = c.fetchone()
        try:
            if r[0] == 'available': # create an appointment
                flag = 1
                c.execute(f"INSERT INTO DENTAL_BOOKING ('client_name','dentist_name', 'time', 'status')\
                            VALUES ('{client_name}', '{dentist_name}', {time}, 'confirmed')")
                
                # update dental_timeslots
                c.execute(f"UPDATE DENTAL_TIMESLOTS set status = 'booked' WHERE dentist_name = '{dentist_name}' AND time = {time};")

                # return booking information
                appointment = dict()
                c.execute(f"SELECT * FROM DENTAL_BOOKING WHERE dentist_name = '{dentist_name}' and time = {time} and status = 'confirmed';")
                result = c.fetchone()
                appointment['booking_id'] = result[0]
                appointment['client_name'] = result[1]
                appointment['dentist_name'] = result[2]
                appointment['time'] = result[3]
                appointment['status'] = result[4]
            elif r[0] == 'booked': # timeslot has been booked
                flag = 2
        except: #timeslot not exist
            flag = 3

        # check DENTAL_BOOKING
        # c.execute(f"SELECT * FROM DENTAL_BOOKING")
        # for i in c.fetchall():
        #     print(i)
        c.close()
        conn.commit()
        conn.close()
        return appointment,flag

    def post(self):
        
        body = g.json
        
        dentist_name = body['dentist_name']
        time = int(body['time'])
        client_name = body['client_name']       

        appointment, flag = self.insert_record('timeslot.db', client_name, dentist_name, time)
        if flag == 1:
            return appointment, 201
        elif flag == 2:
            return {'message': "This timeslot is already booked by another appointment, please select another timeslot"}, 400
        else: 
            return {'message': 'The timeslot you want to book is not exist, please select another timeslot'},404