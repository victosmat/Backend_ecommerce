import random, json, requests
from .models import Inventory
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def initiate(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            resp = {}

            items = Inventory.objects.all()
            if items.count() > 0:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Inventory Existed.'
            else:
                invent = Inventory(
                    address = "",
                    book_quantity = 50000,
                    clothes_quantity = 50000,
                    electronics_quantity = 50000,
                    items = {},
                    status = "Ready"
                )
                invent.save()
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Inventory Initiated.'

            return HttpResponse(json.dumps(resp), content_type='application/json')

    return HttpResponse('Invalid request', status=400)

def get_inventory():
    items = Inventory.objects.all()
    for item in items:
        return item
    return None

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin inventory và sản phẩm cần thêm
            address = data.get('Address')
            book_quant = data.get('Book Quantity')
            clothes_quant = data.get('Clothes Quantity')
            elec_quant = data.get('Electronic Quantity')
            status = data.get('Status')

            try:
                invent = get_inventory()
            except invent == None:
                HttpResponse('Inventory not existed', status=400)

            invent.address = address
            invent.book_quantity = book_quant
            invent.clothes_quantity = clothes_quant
            invent.electronics_quantity = elec_quant
            invent.status = status

            invent.save()

            resp = {}

            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Updated Sucessfully.'

            return HttpResponse(json.dumps(resp), content_type='application/json')

    return HttpResponse('Invalid request', status=400)

def find_item_in_inventory(inventory, product_id):
    for item in inventory.items:
        if item == str(product_id):
            return inventory.items[item]
    return -1

@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin về sản phẩm cần thêm
            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            try:
                inventory = get_inventory()
            except inventory == None:
                HttpResponse('Inventory not existed', status=400)

            quan = find_item_in_inventory(inventory=inventory, product_id=product_id)
            if quan == -1: # Thêm sản phẩm mới vào danh sách items của inventory
                items = inventory.items
                items[product_id] = quantity
                inventory.items = items
                inventory.save()
            else: # Chỉnh sửa số lượng
                for item in inventory.items:
                    if item == str(product_id):
                        inventory.items[item] = inventory.items[item] + quantity
                inventory.save()

            # Trả về thông tin của inventory đã được cập nhật
            response_data = {'Inventory ID': inventory.id, 'Items': inventory.items}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)

@csrf_exempt
def show_inventory(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            try:
                inventory = Inventory.objects.get()
            except Inventory.DoesNotExist:
                return HttpResponse('Inventory not existed', status=404)
            
            items = inventory.items
            response_data = []
            for item in items:
                print(item)
                des = requests.post('http://127.0.0.1:8002/books/books/search/', json={"search_term": int(item)}).json()
                print(des)
                response_data.append({item : {
                        'Description' : des,
                        'Quantity' : items[item]
                    }
                })

            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)

@csrf_exempt
def remove_product(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin inventory và sản phẩm cần xoá
            product_id = data.get('Product ID')
            quantity = data.get('Quantity')

            # Tìm inventory theo inventory_id
            try:
                inventory = Inventory.objects.get()
            except Inventory.DoesNotExist:
                return HttpResponse('Inventory not found', status=404)

            quan = find_item_in_inventory(inventory=inventory, product_id=product_id)
            if quan == -1: # Sản phẩm không tồn tại trong inventory
                return HttpResponse('Item not found', status=404)
            else: # Cập nhật số lượng hoặc xoá sản phẩm
                for item in inventory.items:
                    print(item)
                    if item == str(product_id):
                        new_quantity = inventory.items[item] - quantity
                        if new_quantity > 0:
                            inventory.items[item] = new_quantity
                        else:
                            inventory.items[item] = 0
                
                inventory.save()

            # Trả về thông tin của inventory đã được cập nhật
            response_data = {'Inventory ID': inventory.id, 'Items': inventory.items}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)

@csrf_exempt
def check_availability(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            try:
                inventory = Inventory.objects.get()
            except Inventory.DoesNotExist:
                return HttpResponse('Inventory not found', status=404)

            current_quantity = 0
            for item in inventory.items:
                current_quantity += item['Quantity']

            # Trả về thông tin của inventory đã được cập nhật
            response_data = {'Quantity': inventory.book_quantity, 'Availabile': inventory.book_quantity - current_quantity}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse('Invalid request', status=400)