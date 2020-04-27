from django.urls import path, re_path
from .rest import AutoTokenCreateAPI

urlpatterns = [
    path('token/create.go', AutoTokenCreateAPI.as_view()),
]    