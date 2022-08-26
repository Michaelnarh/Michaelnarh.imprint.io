from .views import index
from django.urls import path

urlpatterns = [
    path("hello/", index)
]
