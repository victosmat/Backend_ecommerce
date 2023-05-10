import random
import json
import requests
from .models import Cart
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def __create_cart(user_id):
    new_cart = Cart(user_id=user_id, items={})
    new_cart.save()
    return new_cart.id


@csrf_exempt
def create_cart(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            user_id = val1.get("User ID")

            if user_id:
                respdata = __create_cart(user_id)
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Added cart.'
                resp['data'] = {'Cart ID': respdata}
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def find_item_in_cart(cart, product_id):
    for item in cart.items:
        if item == str(product_id):
            return cart.items[item]
    return -1


def cart_data_update(cart_id):
    cart = Cart.objects.filter(id=cart_id)
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
def add_item_to_cart(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            user_id = data.get('User ID')
            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            # Tìm cart theo cart_id và user_id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except Cart.DoesNotExist:
                return HttpResponse('Cart not found', status=404)

            quan = find_item_in_cart(cart=cart, product_id=product_id)
            if quan == -1:  # Thêm sản phẩm mới vào danh sách items của cart
                items = cart.items
                items[product_id] = quantity
                # items.append({'Product ID': product_id, 'Quantity': quantity})
                cart.items = items
                cart.save()
            else:  # Chỉnh sửa số lượng
                print(cart.items)
                for item in cart.items:
                    print(item)
                    if item == str(product_id):
                        cart.items[item] = cart.items[item] + quantity
                cart.save()

            # Trả về thông tin của cart đã được cập nhật
            response_data = {'Cart ID': cart.id,
                             'User ID': cart.user_id, 'Items': cart.items}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)


@csrf_exempt
def show_cart(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            user_id = data.get('User ID')

            # Tìm cart theo cart_id và user_id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except Cart.DoesNotExist:
                return HttpResponse('Cart not found', status=404)

            items = cart.items
            response_data = []
            for item in items:
                print(item)
                des = requests.post(
                    'http://127.0.0.1:8002/books/books/search/', json={"search_term": int(item)}).json()
                print(des)
                response_data.append({item: {
                    'Description': des,
                    'Quantity': items[item]
                }
                })

            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)


@csrf_exempt
def remove_item_from_cart(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần xoá
            user_id = data.get('User ID')
            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            # Tìm cart theo cart_id và user_id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except Cart.DoesNotExist:
                return HttpResponse('Cart not found', status=404)

            quan = find_item_in_cart(cart=cart, product_id=product_id)
            if quan == -1:  # Sản phẩm không tồn tại trong cart
                return HttpResponse('Item not found', status=404)
            else:  # Cập nhật số lượng hoặc xoá sản phẩm
                for item in cart.items:
                    if item == str(product_id):
                        new_quantity = cart.items[item] - quantity
                        if new_quantity > 0:
                            cart.items[item] = new_quantity
                        else:
                            cart.items[item] = 0

                cart.save()

            # Trả về thông tin của cart đã được cập nhật
            response_data = {'Cart ID': cart.id,
                             'User ID': cart.user_id, 'Items': cart.items}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)


@csrf_exempt
def clear_cart(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần xoá
            user_id = data.get('User ID')

            # Tìm cart theo cart_id và user_id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except Cart.DoesNotExist:
                return HttpResponse('Cart not found', status=404)

            items = cart.items
            for item in items:
                cart.items[item] = 0

            cart.save()

            # Trả về thông tin của cart đã được cập nhật
            response_data = {'Cart ID': cart.id, 'User ID': cart.user_id,
                             'Items': cart.items, 'Message': 'Cleared cart successfully.'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)
