# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from payment.models import payment_status as paystat
from cart_update.views import order_details_update as order_update
# This function is for fetching the user data.


def get_transaction_details(uname):
    user = paystat.objects.filter(username=uname)
    for data in user.values():
        return data
# This function is used for storing the data.


def store_data(uname, orderid, prodid, price, quantity, mode_of_payment):
    user_data = paystat(username=uname, order_id=orderid, product_id=prodid, price=price, quantity=quantity,
                        mode_of_payment=mode_of_payment, status="Success")
    user_data.save()
    return user_data.id
# This function is created for getting the payment.


@csrf_exempt
def get_payment(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            uname = val1.get('User Name')
            orderid = val1.get('Order id')
            prodid = val1.get('Product id')
            price = val1.get('Product price')
            quantity = val1.get('Product quantity')
            mode_of_payment = val1.get('Payment mode')

            if uname and orderid and prodid and price and quantity and mode_of_payment:
                # It will call the store data function.
                respdata = store_data(uname, orderid, prodid, price,
                                      quantity, mode_of_payment)
                respdata3 = order_update(orderid)

                if respdata:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Added payment.'
                    resp['data'] = {'Payment ID': respdata}

                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'Author existed.'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def user_transaction_info(request):
    # uname = request.POST.get("User Name")
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            uname = val1.get('User Name')
            # uname = request.POST.get("User Name")
            resp = {}
            if uname:
                # Calling the getting the user info.
                respdata = get_transaction_details(uname)
                if respdata:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['data'] = respdata
            # If a user is not found then it give failed as response.
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'User Not Found.'
    # The field value is missing.
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Fields is mandatory.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Request type is not matched.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Request type is not matched.'
    return HttpResponse(json.dumps(resp), content_type='application/json')
