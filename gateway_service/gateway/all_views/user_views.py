import random, json, requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    resp = {}
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)

            # Lấy thông tin cart và sản phẩm cần thêm
            username = data.get('Username')
            password = data.get('Password')
            email = data.get('Email')
            address = data.get('Address')
            city = data.get('City')
            country = data.get('Country')
            first_name = data.get('First Name')
            last_name = data.get('Last Name')

            if username and password and email and address and city and country and first_name and last_name:
                address_id = requests.post('http://127.0.0.1:4000/users/create_address/', json={
                    "Address" : address,
                    "City" : city,
                    "Country" : country
                }).json()
                fullname_id = requests.post('http://127.0.0.1:4000/users/create_fullname/', json={
                    "First Name" : first_name,
                    "Last Name" : last_name
                }).json()
                account_id = requests.post('http://127.0.0.1:4000/users/create_account/', json={
                    "Username" : username,
                    "Password" : password,
                    "Email" : email
                }).json()
                customer_id = requests.post('http://127.0.0.1:4000/users/create_customer/', json={
                    "Address ID" : address_id['data']['Address ID'],
                    "Fullname ID" : fullname_id['data']['Fullname ID'],
                    "Account ID" : account_id['data']['Account ID']
                }).json()
                resp['status'] = 'Success'
                resp['status_code'] = '200'
                resp['message'] = 'Successfully registered.'
                resp['data'] = {
                    "Address" : address_id, 
                    "Fullname" : fullname_id, 
                    "Account": account_id, 
                    "Customer ID" : customer_id
                } 
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'

    return HttpResponse(json.dumps(resp), content_type='application/json')