from django.http import HttpResponse, JsonResponse
from rest_framework import status

class Created(JsonResponse):
    def __init__(self, message, data):
        content = {'success': True, 'message': message, 'data': data}
        super(Created, self).__init__(content, status=201)

class OK(JsonResponse):
    def __init__(self, message, data):
        content = {'success': True, 'message': message, 'data': data}
        super(OK, self).__init__(content, status=200)


class Unauthorised(JsonResponse):
    def __init__(self, message):
        error_key = list(message.keys())[0]
        content = {'success': False, 'message': message[error_key][0], 'data': None}
        super(Unauthorised, self).__init__(content, status=401)

class BadRequest(JsonResponse):
    def __init__(self, message):
        error_key = list(message.keys())[0]
        content = {'success': False, 'message': message[error_key][0], 'data': None}
        super(BadRequest, self).__init__(content, status=400)