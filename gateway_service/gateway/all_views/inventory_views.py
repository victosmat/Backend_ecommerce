import random, json, requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def inititate_inventory(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            requests.post('http://127.0.0.1:8009/inventory/initiate/', json={}).json()

            address = data.get('Address')
            book_quant = data.get('Book Quantity')
            clothes_quant = data.get('Clothes Quantity')
            elec_quant = data.get('Electronic Quantity')
            status = data.get('Status')

            data = requests.post('http://127.0.0.1:8009/inventory/initiate/', json={
                "Address" : address,
                "Book Quantity" : book_quant,
                "Clothes Quantity" : clothes_quant,
                "Electronic Quantity" : elec_quant,
                "Status" : status
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully updated.'
            resp['data'] = data

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def add_product_to_inventory(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            data = requests.post('http://127.0.0.1:8009/inventory/add_product/', json={
                "Product ID" : product_id,
                "Quantity" : quantity
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully added product to inventory.'
            resp['data'] = data

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def remove_product_from_inventory(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            data = requests.post('http://127.0.0.1:8009/inventory/remove_product/', json={
                "Product ID" : product_id,
                "Quantity" : quantity
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully removed product from inventory.'
            resp['data'] = data

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def show_inventory(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            inventory = requests.post('http://127.0.0.1:8009/inventory/show_inventory/', json={}).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully retrived data.'
            resp['data'] = inventory

    return HttpResponse(json.dumps(resp), content_type='application/json')