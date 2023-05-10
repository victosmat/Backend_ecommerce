import random
import json
import requests
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
                    "Category Name": category_name
                }).json()
                category_id = requests.post('http://127.0.0.1:8002/books/categories/search/', json={
                    "Category Name": category_name
                }).json()
                requests.post('http://127.0.0.1:8002/books/authors/create/', json={
                    "Author Name": author_name,
                    "Email": author_email,
                    "Address": author_address,
                }).json()
                author_id = requests.post('http://127.0.0.1:8002/books/authors/search/', json={
                    "Author Name": author_name,
                    "Email": author_email,
                    "Address": author_address,
                }).json()
                book_id = requests.post('http://127.0.0.1:8002/books/books/create/', json={
                    "Author ID": author_id['data'][0]['id'],
                    "Category ID": category_id['data'][0]['id'],
                    "Title": book_title,
                    "Published Date": published_date,
                    "Price": price,
                    "Description": description
                }).json()
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Successfully registered.'
                resp['data'] = {
                    "Author": author_id,
                    "Category": category_id,
                    "Book": book_id
                }
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'

    return HttpResponse(json.dumps(resp), content_type='application/json')
