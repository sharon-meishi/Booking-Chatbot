# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import sqlite3

# cancel appointment with booking id
class TimeslotsDentalCancel(Resource):

    def put(self):
        booking_id = int(g.args.get('booking_Id'))

        conn = sqlite3.connect('timeslot.db')
        c = conn.cursor()        

        # check status of the booking
        c.execute(f'SELECT * FROM DENTAL_BOOKING WHERE booking_id = {booking_id};')
        r = c.fetchone()
        try:
            if r[4] == 'confirmed': # booking exist and haven't been canceled      
                flag = 1
                # cancel the booking 
                c.execute(f"UPDATE DENTAL_BOOKING set status = 'canceled' WHERE booking_id = {booking_id};")
                # update dental_timeslots
                dentist_name = r[2] 
                time = r[3]
                c.execute(f"UPDATE DENTAL_TIMESLOTS set status = 'available' WHERE dentist_name = '{dentist_name}' AND time = {time};")
                # return booking information
                appointment = dict()
                c.execute(f'SELECT * FROM DENTAL_BOOKING WHERE booking_id = {booking_id};')
                result = c.fetchone()
                appointment['booking_id'] = result[0]
                appointment['client_name'] = result[1]
                appointment['dentist_name'] = result[2]
                appointment['time'] = result[3]
                appointment['status'] = result[4]
            elif r[4] == 'canceled': # booking exist but already be canceled
                flag = 2
        except: # booking id not exist 
            flag = 3


        # check DENTAL_BOOKING
        # c.execute(f"SELECT * FROM DENTAL_BOOKING")
        # for i in c.fetchall():
        #     print(i)
        c.close()
        conn.commit()
        conn.close()
        if flag == 1:
            return appointment, 201 
        elif flag == 2:
            return {'message': "The appointment has already been canceled before"}, 400
        else:
            return {'message': "The appointment you want to cancel is not exist, please enter another booking id "}, 404