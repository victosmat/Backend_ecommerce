import random, json, requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_book(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            category_name = data.get('Category Name')
            author_name = data.get('Author Name')
            author_email = data.get('Author Email')
            author_address = data.get('Author Address')
            book_title = data.get('Book Title')
            published_date = data.get('Publishded Date')
            price = data.get('Price')
            description = data.get('Description')

            if category_name and author_name and author_email and author_address and book_title and published_date and price and description:
                requests.post('http://127.0.0.1:8002/books/categories/create/', json={
                    "Category Name" : category_name
                }).json()
                category_id = requests.post('http://127.0.0.1:8002/books/categories/search/', json={
                    "Category Name" : category_name
                }).json()
                requests.post('http://127.0.0.1:8002/books/authors/create/', json={
                    "Author Name" : author_name,
                    "Email" : author_email,
                    "Address" : author_address,
                }).json()
                author_id = requests.post('http://127.0.0.1:8002/books/authors/search/', json={
                    "Author Name" : author_name,
                    "Email" : author_email,
                    "Address" : author_address,
                }).json()
                book_id = requests.post('http://127.0.0.1:8002/books/books/create/', json={
                    "Author ID" : author_id['data'][0]['id'],
                    "Category ID" : category_id['data'][0]['id'],
                    "Title" : book_title,
                    "Published Date" : published_date,
                    "Price" : price,
                    "Description" : description
                }).json()
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Successfully registered.'
                resp['data'] = {
                    "Author" : author_id, 
                    "Category" : category_id, 
                    "Book" : book_id
                } 
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def register_shoes(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            # Name, Brand ID,  Color, Size, Price, Description
            p_name = data.get('Product Name')
            b_name = data.get('Brand Name')
            color = data.get('Color')
            size = data.get('Size')
            price = data.get('Price')
            description = data.get('Description')

            if p_name and b_name and color and size and price and description:
                requests.post('http://127.0.0.1:2200/shoes/create_brand/', json={
                    "Brand Name" : b_name
                }).json()
                brand_id = requests.get('http://127.0.0.1:2200/shoes/search_brand/', json={
                    "Brand Name" : b_name
                }).json()
                requests.post('http://127.0.0.1:2200/shoes/create_shoe/', json={
                    "Name" : p_name,
                    "Brand ID" : brand_id['ID'],
                    "Color" : color,
                    "Size" : size,
                    "Price" : price,
                    "Description" : description
                }).json()
                shoes_id = requests.get('http://127.0.0.1:2200/shoes/search_shoe/', json={
                    "Shoe Name" : p_name,
                }).json()
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Successfully registered.'
                resp['data'] = {
                    "Brand" : brand_id, 
                    "Shoes" : shoes_id, 
                } 
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def register_clothes(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            # Name, Brand ID,  Category, Size, Price, Description
            p_name = data.get('Product Name')
            b_name = data.get('Brand Name')
            category = data.get('Category')
            size = data.get('Size')
            price = data.get('Price')
            description = data.get('Description')
            if p_name and b_name and category and size and price and description:
                requests.post('http://127.0.0.1:2300/clothes/create_brand/', json={
                    "Brand Name" : b_name
                }).json()
                brand_id = requests.get('http://127.0.0.1:2300/clothes/search_brand/', json={
                    "Brand Name" : b_name
                }).json()
                print(brand_id)
                shoes_id = requests.post('http://127.0.0.1:2300/clothes/create_clothing/', json={
                    "Name" : p_name,
                    "Brand ID" : brand_id['ID'],
                    "Category" : category,
                    "Size" : size,
                    "Price" : price,
                    "Description" : description
                }).json()
                print(shoes_id)
                shoes_id = requests.get('http://127.0.0.1:2300/clothes/search_clothing/', json={
                    "Clothing Name" : p_name,
                }).json()
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Successfully registered.'
                resp['data'] = {
                    "Brand" : brand_id, 
                    "Shoes" : shoes_id, 
                } 
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'

    return HttpResponse(json.dumps(resp), content_type='application/json')