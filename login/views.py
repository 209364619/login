"""
time: 2019/9/9 
author：hph
"""
from django.http import request
from django.http import JsonResponse
from django.http import HttpResponse
from login.jwt_moudle import JwtMoudle
import json

from login.auth_permission import auth_permission_required
from login.user_in_mongo import User
@auth_permission_required(['superadmin'])
def hello_test(request):
    return HttpResponse('Hello World')
def login(request):
    data = json.loads(request.body.decode())
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User()
        user = user.search_user_by_name_and_password(username,password)

        if user:
            jwt = JwtMoudle()
            data = {'username': username,'role':user.get('role')}
            token = jwt.get_token(data)
            return JsonResponse({'status':1,'token':token})
        else:
            return JsonResponse({'status':0,'msg':'user does not exist or password error'})
    return JsonResponse({'status':0,'msg':'please input your username and password'})


def register(request):
    pass



#using token, need not to logout
def logout():
    pass