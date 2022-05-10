from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from core.views import SignInView, LoginView, RetrieveUpdateProfileView, UpdatePassword  # DestroyProfileView

urlpatterns = [
    path("signup", SignInView.as_view()),
    path("login", csrf_exempt(LoginView)),
    # path("delete", DestroyProfileView.as_view()),
    path("profile", RetrieveUpdateProfileView.as_view()),
    path("update_password", UpdatePassword.as_view()),
    ]
