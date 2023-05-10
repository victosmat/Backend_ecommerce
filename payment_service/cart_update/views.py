# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from payment.models import payment_status as paystat
import requests
import json
# This function is for fetching the user data.


def order_details_update(id):
    ship_dict = {}
    ship_dict['Order ID'] = id
    ship_dict['Status'] = 'Shipped'

    # Data is ready for calling the shipment_updates API.
    url = 'http://127.0.0.1:8008/orders/update_order/'
    data = json.dumps(ship_dict)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    api_resp = json.loads(response.content.decode('utf-8'))
    return api_resp
