import random, json, requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_product_to_cart(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            user_id = data.get('User ID')
            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            data = requests.post('http://127.0.0.1:5000/carts/add_item_to_cart/', json={
                "User ID" : user_id,
                "Product ID" : product_id,
                "Quantity" : quantity
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully added product to cart.'
            resp['data'] = data

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def remove_item_from_cart(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần xoá
            user_id = data.get('User ID')
            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            data = requests.post('http://127.0.0.1:5000/carts/remove_item_from_cart/', json={
                "User ID" : user_id,
                "Product ID" : product_id,
                "Quantity" : quantity
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully removed product from cart.'
            resp['data'] = data

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def show_cart(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            user_id = data.get('User ID')

            cart = requests.post('http://127.0.0.1:5000/carts/show_cart/', json={
                "User ID" : user_id
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully retrived information.'
            resp['data'] = cart

    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def purchase(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            user_id = data.get('User ID')

            order_id = requests.post('http://127.0.0.1:3000/orders/create_order/', json={
                "User ID" : user_id
            }).json()

            requests.post('http://127.0.0.1:5000/carts/clear_cart/', json={
                "User ID" : user_id
            }).json()

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Successfully retrieved information.'
            resp['data'] = {"Order ID" : order_id}

    return HttpResponse(json.dumps(resp), content_type='application/json')