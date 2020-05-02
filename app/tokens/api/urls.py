from django.urls import path, re_path
from app.tokens.api.rest import TokenCreateAPI, TokenGetAPI

urlpatterns = [
    path('create.go', TokenCreateAPI.as_view()),
    path('list.go', TokenGetAPI.as_view()),
]