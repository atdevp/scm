from django.urls import path

from app.menu.api.rest import MenuListAPI

urlpatterns = [
    path('list.go', MenuListAPI.as_view()),
]