from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from myapp.models import Book
from myapp.serializer import BookSerializer


# Create your views here.
# DELTE도 만들어서 전체 삭제기능 만들기
@api_view(["GET", "POST", "PUT"])
def getResource(request):
    if request.method == "GET":
        data = Book.objects.all()
        serializedData = BookSerializer(data=data, many=True)
        # is_valid를 하지않으면 AssertionError가 나와서 임시방편으로 넣음
        print(serializedData.is_valid())
        # 한글이 나오지않는 문제가 생김
        return JsonResponse({'data': serializedData.data})

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializedData = BookSerializer(data=data)
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        print("data: ", data)
        if Book.objects.get(name=data["name"]) is not None:
            query = Book.objects.get(name=data["name"])
            serializedData = BookSerializer(query, data=data)
            if serializedData.is_valid():
                serializedData.save()
                return JsonResponse({'success': True, 'data': serializedData.data})
            else:
                return JsonResponse({'success': False, 'data': None})
        else:
            return JsonResponse({'success': False, 'data': None})


@api_view(["DELETE"])
def deleteResource(request, primary_key):
    if request.method == "DELETE":
        try:
            data = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            return JsonResponse({"message": "does not exist"})
        data.delete()
        return JsonResponse({"success": True})
