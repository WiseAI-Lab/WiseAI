from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r"^get_auth_token$", views.get_auth_token, name="get_auth_token"),
    url(r"^register$", views.CreateUserAPIView.as_view(), name="register"),
]
app_name = "accounts"
