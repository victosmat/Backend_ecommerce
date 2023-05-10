import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Brand, Clothing


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
def create_clothing(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('Name')
        brand_id = data.get('Brand ID')
        category = data.get('Category')
        size = data.get('Size')
        price = data.get('Price')
        description = data.get('Description')

        for val in Clothing.objects.filter(name=name).all():
            return JsonResponse({'error': 'Product existed!'})

        if name and brand_id and category and size and price and description:
            brand = Brand.objects.get(id=brand_id)
            clothing = Clothing(name=name, brand=brand, category=category,
                                size=size, price=price, description=description)
            clothing.save()
            return JsonResponse({'message': 'Clothing created successfully!',
                                 'description': {
                                     'ID': clothing.id,
                                     'Name': name,
                                     'Brand': brand.id,
                                     'Category': category,
                                     'Size': size,
                                     'Price': price,
                                     'Description': description
                                 }})
        else:
            return JsonResponse({'error': 'Please provide all fields!'})


@csrf_exempt
def delete_brand(request, brand_id):
    if request.method == 'DELETE':
        try:
            brand = Brand.objects.get(id=brand_id)
            brand.delete()
            return JsonResponse({'message': 'Brand deleted successfully!',
                                 'description': {'ID': brand_id}
                                 })
        except Brand.DoesNotExist:
            return JsonResponse({'error': 'Invalid brand id!'})


@csrf_exempt
def delete_clothing(request, clothing_id):
    if request.method == 'DELETE':
        try:
            clothing = Clothing.objects.get(id=clothing_id)
            clothing.delete()
            return JsonResponse({'message': 'Clothing deleted successfully!',
                                 'description': {'ID': clothing_id}
                                 })
        except Clothing.DoesNotExist:
            return JsonResponse({'error': 'Invalid clothing id!'})


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
def search_clothing(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        name = data.get('Clothing Name')
        try:
            clothes = Clothing.objects.filter(name__icontains=name)
            data = []
            for clothing in clothes:
                data.append({'ID': clothing.id, 'Name': clothing.name, 'Brand': clothing.brand.name, 'Category': clothing.category,
                             'Size': clothing.size, 'Price': str(clothing.price), 'Description': clothing.description})
            return JsonResponse(data, safe=False)
        except Clothing.DoesNotExist:
            return JsonResponse({'error': 'Clothes not found!'})
