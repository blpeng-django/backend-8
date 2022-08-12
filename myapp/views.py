from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from myapp.models import Book
from myapp.serializer import BookSerializer


@api_view(["GET"])
def getResource(resource):
    if resource.method == "GET":
        data = Book.objects.all()
        # many는 all을 통해 여러 데이터를 가져온 경우 사용해야하는 옵션인것 같음
        serializedData = BookSerializer(data=data, many=True)
        serializedData.is_valid()
        return JsonResponse({"data": serializedData.data}, json_dumps_params={'ensure_ascii': False})


@api_view(["POST"])
def postResource(resource):
    if resource.method == "POST":
        data = JSONParser().parse(resource)
        serializedData = BookSerializer(data=data)
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})


@api_view(["PUT"])
def putResource(resource):
    if resource.method == "PUT":
        data = JSONParser().parse(resource)
        query = Book.objects.get(pk=data["name"])
        # 데이터가 중복되면 is_valid를 통과하지 못하는데 query를 넣으면 해결되는 것 같음.
        # serializedData = BookSerializer(query, data=query) 에러가 나오지 않음.
        # get에서도 같은 방식으로하면 해결할 수 있을것 같아 시도해봤지만 정상작동 X, 여러 데이터를 받았을때에는 또 다른 예외가 발생하는 것 같음.
        serializedData = BookSerializer(query, data=data)
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})


@api_view(["DELETE"])
def deleteResource(resource, primaryKey=None):
    if resource.method == "DELETE":
        # 하나의 데이터 지우기
        if primaryKey:
            data = Book.objects.get(pk=primaryKey)
            data.delete()
            return JsonResponse({"success": True})
        # 모든 데이터 지우기
        else:
            data = Book.objects.all()
            data.delete()
            return JsonResponse({"success": True})
