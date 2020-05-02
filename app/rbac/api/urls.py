from  .rest import RolesAPIView
from django.urls import path

urlpatterns = [
    path('role/create.go', RolesAPIView.as_view()), 
]