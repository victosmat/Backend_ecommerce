import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Brand, Shoe


@csrf_exempt
def create_brand(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('Brand Name')
        if name:
            for val in Brand.objects.filter(name=name).all():
                return JsonResponse({'error': 'Brand existed!'})
            brand = Brand(name=name)
            brand.save()
            return JsonResponse({'message': 'Brand created successfully!',
                                 'description': {
                                     'ID': brand.id,
                                     'Brand Name': name
                                 }})
        else:
            return JsonResponse({'error': 'Please provide name!'})


@csrf_exempt
def create_shoe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('Name')
        brand_id = data.get('Brand ID')
        color = data.get('Color')
        size = data.get('Size')
        price = data.get('Price')
        description = data.get('Description')
        for val in Shoe.objects.filter(name=name).all():
            return JsonResponse({'error': 'Shoe existed!'})

        if name and brand_id and color and size and price and description:
            try:
                brand = Brand.objects.get(id=brand_id)
                shoe = Shoe(name=name, brand=brand, color=color,
                            size=size, price=price, description=description)
                shoe.save()
                return JsonResponse({'message': 'Shoe created successfully!',
                                     'description': {
                                         'ID': shoe.id,
                                         'Name': name,
                                         'Brand ID': brand.id,
                                         'Color': color,
                                         'Size': size,
                                         'Price': price,
                                         'Description': description
                                     }})
            except Brand.DoesNotExist:
                return JsonResponse({'error': 'Invalid brand id!'})
        else:
            return JsonResponse({'error': 'Please provide all fields!'})


@csrf_exempt
def delete_brand(request, brand_id):
    if request.method == 'DELETE':
        try:
            brand = Brand.objects.get(id=brand_id)
            brand.delete()
            return JsonResponse({'message': 'Brand deleted successfully!',
                                 'description': {
                                     'ID': brand_id
                                 }
                                 })
        except Brand.DoesNotExist:
            return JsonResponse({'error': 'Invalid brand id!'})


@csrf_exempt
def delete_shoe(request, shoe_id):
    if request.method == 'DELETE':
        try:
            shoe = Shoe.objects.get(id=shoe_id)
            shoe.delete()
            return JsonResponse({'message': 'Shoe deleted successfully!',
                                 'description': {
                                     'ID': shoe_id
                                 }
                                 })
        except Shoe.DoesNotExist:
            return JsonResponse({'error': 'Invalid shoe id!'})


@csrf_exempt
def search_brand(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        name = data.get('Brand Name')
        try:
            brand = Brand.objects.get(name=name)
            data = {'ID': brand.id, 'Name': brand.name}
            return JsonResponse(data)
        except Brand.DoesNotExist:
            return JsonResponse({'error': 'Brand not found!'})


@csrf_exempt
def search_shoe(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        name = data.get('Shoe Name')
        if name:
            try:
                shoes = Shoe.objects.filter(name__icontains=name)
                data = []
                for shoe in shoes:
                    data.append({'ID': shoe.id, 'Name': shoe.name, 'Brand': shoe.brand.name, 'Color': shoe.color,
                                'Size': shoe.size, 'Price': str(shoe.price), 'Description': shoe.description})
                return JsonResponse(data, safe=False)
            except Shoe.DoesNotExist:
                return JsonResponse({'error': 'Shoe not found!'})
    return JsonResponse({'error': 'Invalid request!'})
