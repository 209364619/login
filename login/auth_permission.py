from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import jwt, time


def auth_permission_required(perm):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            try:
                auth = request.META.get('HTTP_AUTHORIZATION').split()
            except AttributeError:
                return JsonResponse({"code": 401, "message": "No authenticate header"})

            # 用户通过 API 获取数据验证流程
            if auth[0].lower() == 'token':
                try:
                    token = jwt.decode(auth[1], 'secret_key', algorithms=['HS256'])
                    end_time = token.get('end_time')
                    now_time = int(time.time())
                    username = token.get('username')
                    role = token.get('role')
                    if end_time < now_time:
                        return JsonResponse(({"status": 0, "message": "Certification expires"}))
                    if role not in perm:
                        return JsonResponse({'status':0,'msg':'Permission denied'})
                except jwt.ExpiredSignatureError:
                    return JsonResponse({"status_code": 401, "message": "Token expired"})
                except jwt.InvalidTokenError:
                    return JsonResponse({"status_code": 401, "message": "Invalid token"})
                except Exception as e:
                    return JsonResponse({"status_code": 401, "message": str(e)})
            else:
                return JsonResponse({"status_code": 401, "message": "Not support auth type"})

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator