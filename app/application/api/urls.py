from django.urls import path, re_path
from app.application.api.rest import ApplicationListAPI, ApplicationCreateAPI


urlpatterns = [
    path('list.go', ApplicationListAPI.as_view()),
    path('create.go', ApplicationCreateAPI.as_view()),

]