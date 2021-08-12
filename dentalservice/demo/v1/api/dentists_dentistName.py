# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import sqlite3

class DentistsDentistname(Resource):

    def get(self, dentistName):
        conn = sqlite3.connect('DentalService.db')
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM DENTALINFO WHERE dentist_name = '{dentistName}'")
            result = c.fetchall()[0]
            dentist = dict()
            dentist['id'] = result[0]
            dentist['name'] = result[1]
            dentist['location'] = result[2]
            dentist['specialization']  = result[3]
            dentist['phone'] = result[4]
            c.close()
            conn.close()
        except Exception as e:
            #print(e)
            c.close()
            conn.close()
            return None, 404
        return dentist, 200