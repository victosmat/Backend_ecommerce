from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from cart_status.models import cart as cartstat

# Create your views here.


def get_transaction_details(uname):
    cart = cartstat.objects.filter(username=uname)
    for data in cart.values():
        return data


def store_data(uname, product_id, quantity):
    cart = cartstat(username=uname, product_id=product_id,
                    quantity=quantity, status="Unpaid")
    cart.save()
    return 1


def get_transaction_details(uname):
    cart = cartstat.objects.filter(username=uname)
    for data in cart.values():
        return data


def cart_data_update(cart_id):
    cart = cartstat.objects.filter(id=cart_id)
    cart.update(status="Paid")
    return 1


@csrf_exempt
def cart_reg_update(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            # This is for reading the inputs from JSON.
            cart_id = val1.get("Cart id")
            resp = {}
        # After all validation, it will call the data_insertfunction.
            respdata = cart_data_update(cart_id)
    # If it returns value then will show success.
            if respdata:
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Product is ready to dispatch.'
                # If value is not found then it will give failed in response.
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Failed to update shipment details.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def get_cart(request):
    uname = request.POST.get('username')
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    resp = {}
    if uname and product_id and quantity:
        respdata = store_data(uname, product_id, quantity)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Transaction is completed.'
    # If it is returning null value then it will show failed.
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Transaction is failed, Please try again.'
    # If any mandatory field is missing then it will be through a failed message.
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def cart_transaction_info(request):
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
