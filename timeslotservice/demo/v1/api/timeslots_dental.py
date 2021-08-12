# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import sqlite3

class TimeslotsDental(Resource):

    def get(self):
        dentist_name = g.args.get('dentist_name')
        #print(dentist_name)
        conn = sqlite3.connect('timeslot.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM DENTAL_TIMESLOTS WHERE dentist_name = '{dentist_name}' and status = 'available'")
        all_timeslot = []
        for i in c.fetchall():
            #print(i)
            timeslot = dict()
            timeslot['dentist_name'] = i[2]
            timeslot['time']  = str(i[3])
            timeslot['status'] = i[4]
            all_timeslot.append(timeslot)
        c.close()
        conn.close()
        #print(all_timeslot)
        if all_timeslot:
            return all_timeslot, 200
        else:
            return {'message':'Dentist not exist'}, 404