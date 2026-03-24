from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import json


@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST allowed"})

    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
    except Exception:
        return JsonResponse({"success": False, "message": "Invalid JSON"})

    user = authenticate(request, username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        return JsonResponse({
            "success": True,
            "message": "Login successful",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "is_superuser": user.is_superuser,
            }
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid username or password"
    })