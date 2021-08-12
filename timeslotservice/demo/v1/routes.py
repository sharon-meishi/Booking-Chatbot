# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.timeslots_dental import TimeslotsDental
from .api.timeslots_dental_reserve import TimeslotsDentalReserve
from .api.timeslots_dental_cancel import TimeslotsDentalCancel


routes = [
    dict(resource=TimeslotsDental, urls=['/timeslots/dental'], endpoint='timeslots_dental'),
    dict(resource=TimeslotsDentalReserve, urls=['/timeslots/dental/reserve'], endpoint='timeslots_dental_reserve'),
    dict(resource=TimeslotsDentalCancel, urls=['/timeslots/dental/cancel'], endpoint='timeslots_dental_cancel'),
]