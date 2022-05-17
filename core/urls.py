from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from core.views import SignInView, LoginView, RetrieveUpdateProfileView, UpdatePassword  # DestroyProfileView

urlpatterns = [
    path("signup", csrf_exempt(SignInView.as_view())),
    path("login", csrf_exempt(LoginView)),
    path("profile", csrf_exempt(RetrieveUpdateProfileView.as_view())),
    path("update_password", csrf_exempt(UpdatePassword.as_view())),
    ]
