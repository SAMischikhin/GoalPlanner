from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from core.views import SignInView, my_view, MyLoginView
from django.contrib.auth import views, authenticate

urlpatterns = [
    path("signup", SignInView.as_view()),
    # path("login", csrf_exempt(views.LoginView.as_view())),
    path("login", csrf_exempt(my_view)),
    # path("login", csrf_exempt(MyLoginView.as_view())),
]
