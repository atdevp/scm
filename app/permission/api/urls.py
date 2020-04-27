from django.urls import path, re_path
from .rest import AutoTokenCreateAPI
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('token/create.go', csrf_exempt(AutoTokenCreateAPI.as_view())),
]    