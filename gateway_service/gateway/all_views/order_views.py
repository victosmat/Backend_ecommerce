import random, json, requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def track_order(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            order_id = data.get('Order ID')

            order = requests.post('http://127.0.0.1:3000/orders/show_order/', json={
                "Order ID" : order_id
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully retrieved information.'
            resp['data'] = {"Order information" : order}

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def update_order(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            order_id = data.get('Order ID')
            status = data.get('Status')

            requests.post('http://127.0.0.1:3000/orders/show_order/', json={
                "Order ID" : order_id,
                'Status' : status
            }).json()

            order = requests.post('http://127.0.0.1:3000/orders/show_order/', json={
                "Order ID" : order_id
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully updated information.'
            resp['data'] = {"Order information" : order}

    return HttpResponse(json.dumps(resp), content_type='application/json')