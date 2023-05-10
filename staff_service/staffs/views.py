from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .models import Account, FullName, Address, Customer


def __create_account(username, password, email):
    new_account = Account(username=username, password=password, email=email)
    new_account.save()
    return new_account.id

@csrf_exempt
def create_account(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            username = val1.get("Username")
            password = val1.get("Password")
            email = val1.get("Email")

            if username and password and email:
                respdata = __create_account(username, password, email)
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Added account.'
                resp['data'] = {'Account ID': respdata}
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __delete_account(account_id):
    account = Account.objects.filter(id=account_id).first()
    if account:
        account.delete()
        return True
    else:
        return False


@csrf_exempt
def delete_account(request, account_id):
    resp = {}
    if request.method == 'DELETE':
        respdata = __delete_account(account_id)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Account deleted successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Account not found.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __create_fullname(first_name, last_name):
    new_fullname = FullName(first_name=first_name, last_name=last_name)
    new_fullname.save()
    return new_fullname.id


@csrf_exempt
def create_fullname(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            first_name = val1.get("First Name")
            last_name = val1.get("Last Name")

            if first_name and last_name:
                respdata = __create_fullname(first_name, last_name)
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Added fullname.'
                resp['data'] = {'Fullname ID': respdata}
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __create_address(address, city, country):
    new_address = Address(address=address, city=city, country=country)
    new_address.save()
    return new_address.id


@csrf_exempt
def create_address(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            address = val1.get("Address")
            city = val1.get("City")
            country = val1.get("Country")

            if address and city and country:
                respdata = __create_address(address, city, country)
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Added address.'
                resp['data'] = {'Address ID': respdata}
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __create_customer(account_id, full_name_id, address_id, role):
    new_customer = Customer(account_id=account_id,
                            full_name_id=full_name_id, address_id=address_id, role=role)
    new_customer.save()
    return new_customer.id


@csrf_exempt
def create_customer(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            account_id = val1.get("Account ID")
            full_name_id = val1.get("Fullname ID")
            address_id = val1.get("Address ID")
            role = val1.get("Role")

            if account_id and full_name_id and address_id:
                respdata = __create_customer(
                    account_id, full_name_id, address_id , role)
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Added customer.'
                resp['data'] = {'Customer ID': respdata}
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __delete_customer(customer_id):
    customer = Customer.objects.filter(id=customer_id).first()
    if customer:
        customer.delete()
        return True
    else:
        return False


@csrf_exempt
def delete_customer(request, customer_id):
    resp = {}
    if request.method == 'DELETE':
        respdata = __delete_customer(customer_id)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Customer deleted successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Customer not found.'
    return HttpResponse(json.dumps(resp), content_type='application/json')
