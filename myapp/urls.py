from .views import allResource, aResource
from django.urls import path

urlpatterns = [
    path('', allResource),
    path('<primary_key>', aResource),
]
