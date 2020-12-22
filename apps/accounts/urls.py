from django.conf.urls import url
from rest_framework_jwt.views import verify_jwt_token

from . import views

urlpatterns = [
    url(r'^register$', views.CreateUserAPIView.as_view()),
    url(r'^info$', views.UserInfoAPIView.as_view()),
    url(r'^login$', views.authenticate_user),
    url(r'^verify$', verify_jwt_token),
    url(r'^update$', views.UserRetrieveUpdateAPIView.as_view()),
]
app_name = "accounts"
