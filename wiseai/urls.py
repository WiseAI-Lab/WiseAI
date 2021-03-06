"""wiseai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

swagger_api_info = openapi.Info(
    title="WiseAI API",
    default_version="v1",
    description="WiseAI Documentation",
    contact=openapi.Contact(email="sfreebobo@163.com"),
    license=openapi.License(name="BSD License"),
)

schema_view = get_schema_view(
    public=True, permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/agent/', include('agents.urls')),
    url(r"^api/auth/", include("dj_rest_auth.urls")),
    url(r"^api/auth/", include("accounts.urls")),
    url(
        r"^api/docs/docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-yaml",
    ),
    url(r'^api/swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(
        r"^api/docs/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    )
]
