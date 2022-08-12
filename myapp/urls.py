from .views import getResource, postResource, putResource, deleteResource
from django.urls import path

urlpatterns = [
    path('/get', getResource),
    path('/post', postResource),
    path('/put', putResource),
    path('/delete/<primaryKey>', deleteResource),
    path('/delete', deleteResource)
]
