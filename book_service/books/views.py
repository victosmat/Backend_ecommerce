from .models import Author, Category, Book
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Q
import json
import random


def __create_author(name, email, address):
    for val in Author.objects.filter(name=name).all():
        return 0
    new_author = Author(name=name, email=email, address=address)
    new_author.save()
    return new_author.id


@csrf_exempt
def create_author(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            name = val1.get("Author Name")
            email = val1.get("Email")
            address = val1.get("Address")

            if name and email and address:
                respdata = __create_author(name, email, address)
                # If it returns value then will show success.
                if respdata:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Added author.'
                    resp['data'] = {'Author ID': respdata}
                    # If value is not found then it will give failed in response.
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'Author existed.'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __create_category(name):
    for val in Category.objects.filter(name=name).all():
        return 0
    new_category = Category(name=name)
    new_category.save()
    return new_category.id


@csrf_exempt
def create_category(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            name = val1.get("Category Name")

            if name:
                respdata = __create_category(name)
                if respdata:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Added category.'
                    resp['data'] = {'Category ID': respdata}
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'Category existed.'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __create_book(title, author_id, category_id, published_date, price, description):
    new_book = Book(title=title, author_id=author_id, category_id=category_id,
                    published_date=published_date, price=price, description=description)
    new_book.save()
    return new_book.id


@csrf_exempt
def create_book(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            title = val1.get("Title")
            author_id = val1.get("Author ID")
            category_id = val1.get("Category ID")
            published_date = val1.get("Published Date")
            price = val1.get("Price")
            description = val1.get("Description")

            if title and author_id and category_id and published_date and price and description:
                respdata = __create_book(
                    title, author_id, category_id, published_date, price, description)
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Added book.'
                resp['data'] = {'Book ID': respdata}
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


def __delete_book(book_id):
    book = Book.objects.filter(id=book_id).first()
    if book:
        book.delete()
        return True
    else:
        return False


@csrf_exempt
def delete_book(request, book_id):
    resp = {}
    if request.method == 'DELETE':
        respdata = __delete_book(book_id)
        if respdata:
            resp['status'] = 'Success'
            resp['status_code'] = '200'
            resp['message'] = 'Book deleted successfully.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Book not found.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def author_search(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            name = val1.get("Author Name")

            if name:
                authors = Author.objects.filter(name__icontains=name).values(
                    'id', 'name', 'email', 'address')
                if authors:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Authors Found.'
                    resp['data'] = list(authors)
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'No authors found.'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Name field is mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def category_search(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            name = val1.get("Category Name")

            if name:
                categories = Category.objects.filter(
                    name__icontains=name).values('id', 'name')
                if categories:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Categories Found.'
                    resp['data'] = list(categories)
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'No categories found.'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Name field is mandatory.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def book_search(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)

            search_term = val1.get("search_term")

            if search_term:
                books = Book.objects.filter(Q(id__icontains=search_term) | Q(title__icontains=search_term) | Q(
                    author__name__icontains=search_term) | Q(category__name__icontains=search_term))
                books_list = []
                for book in books:
                    book_dict = {}
                    book_dict['id'] = book.id
                    book_dict['title'] = book.title
                    book_dict['author'] = book.author.name
                    book_dict['category'] = book.category.name
                    book_dict['published_date'] = book.published_date.strftime(
                        '%Y-%m-%d')
                    book_dict['price'] = str(book.price)
                    book_dict['description'] = book.description
                    books_list.append(book_dict)

                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Books retrieved successfully'
                resp['data'] = books_list
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Search term is required.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Invalid content type.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Invalid request method.'

    return HttpResponse(json.dumps(resp), content_type='application/json')
