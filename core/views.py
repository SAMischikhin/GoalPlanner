import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.models import User
from core.serializers import UserRegistrationSerializer, RetrieveUpdateProfileSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, logout


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


def LoginView(request):
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
            return 404


class RetrieveUpdateProfileView(RetrieveUpdateAPIView):
    # authentication_classes = SessionAuthentication#(SessionAuthentication, TokenAuthentication)
    serializer_class = RetrieveUpdateProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse('log out', safe=False, status=204)


# class DestroyProfileView(RetrieveUpdateDestroyAPIView):
#     serializer_class = RetrieveUpdateProfileSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_object(self):
#         return self.request.user
#
#     def delete(self, request, *args, **kwargs):
#         logout(request)
#
#         return self.destroy(request, *args, **kwargs)

class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            # return Response(status=status.HTTP_204_NO_CONTENT)
            return JsonResponse(
                {
                    "old_password": serializer.data["old_password"],
                    "new_password":  serializer.data["new_password"],
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)