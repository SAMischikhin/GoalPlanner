import json

from django.http import JsonResponse
from django.views.generic import CreateView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login


class SignInView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse({
               "id": response.data["id"],
                "username": response.data["username"],
                "first_name": response.data["first_name"],
                "last_name": response.data["last_name"],
                "email": response.data["email"],
                "password": request.data["password"],
                "password_repeat": request.data["password_repeat"],
            }
        )

def my_view(request):
    if request.method == 'POST':
        body_data = json.loads(request.body)
        username = body_data['username']
        password = body_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return JsonResponse(
                {
                    "username": user.username,
                    "password": user.password,
                }
            )
        else:
            raise AuthenticationFailed(detail=None, code=404)

class MyLoginView(CreateView):
    pass
#     model = User
#
#     def post(self, request, *args, **kwargs):
#
#         username = self.request.body['username']
#         password = self.request.body['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#
#         return JsonResponse(
#             {
#                 "username": self.object.id,
#                 "password": self.object.name,
#             }
#         )