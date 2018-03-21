from django.test import TestCase
from rest_framework.test import APIClient
import json
from urllib.request import Request, urlopen

# Create your tests here.
class TestUserCreate(TestCase):

    def test_user_create_fail(self):
        ''' tests the user createion fail
        '''  
        client = APIClient()
        request = client.post('/api/user/new',
                    '{"username":"rahul","password":"hello"}',
                    content_type="application/json")
        self.assertEqual(request.status_code, 400)


    def test_user_login_fail(self):
        ''' user login fail
        '''
        client = APIClient()
        data = {"username": "rahul", "password": "hell"}
        data = json.dumps(data)
        request = client.post('/api/login', data,
                               content_type="application/json")
        self.assertEqual(request.status_code, 400)
        resp = json.loads(request.content.decode('utf-8'))
        #print(resp)
        message = 'user doesnot exists'
        self.assertEqual(resp['message'], message)

    
    def test_user_login_success(self):
        ''' user login success
        '''
        client = APIClient()
        data = {"username":"rahul", "password":"hello"}
        request = client.post('/api/login', json.dumps(data),
                               format="json")
        #url = '/api/login'
        #req = Request(url,json.dumps(data))
        #resp = urlopen(req)
        #print(resp)
        self.assertNotEqual(request.status_code, 200)


    def test_user_logout_fail(self):
        '''user login fails
        '''
        client = APIClient()
        #header = {'Authorization': 'Token aereefefer454676g535g'}
        client.credentials(HTTP_AUTHORIZATION='Token '+ 'sasas')
        request = client.get('/api/logout')
        self.assertEqual(request.status_code, 401)