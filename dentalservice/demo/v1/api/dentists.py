# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import sqlite3

class Dentists(Resource):

    def get(self):
        conn = sqlite3.connect('DentalService.db')
        c = conn.cursor()
        c.execute("SELECT * FROM DENTALINFO;")
        all_dentist = []
        for i in c.fetchall():
            dentist = dict()
            dentist['id'] = str(i[0])
            dentist['name'] = i[1]
            dentist['location'] = i[2]
            dentist['specialization']  = i[3]
            all_dentist.append(dentist)
        c.close()
        conn.close()

        answer = all_dentist
        return answer, 200