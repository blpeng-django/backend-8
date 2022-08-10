from .views import deleteResource, getResource
from django.urls import path

urlpatterns = [
    path('', getResource),
    path('<primary_key>', deleteResource),
]
