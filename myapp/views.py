from tempfile import TemporaryFile
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from myapp.models import Book
from myapp.serializer import BookSerializer


@api_view(["GET", "POST", "PUT", "DELETE"])
def allResource(request):
    if request.method == "GET":
        data = Book.objects.all()
        serializedData = BookSerializer(data=data, many=True)
        if serializedData.is_valid(raise_exception=True):
            # 한글이 유니코드로 변하는 문제를 json_dumps_params={'ensure_ascii': False}로 해결함
            return JsonResponse({'data': serializedData.data, 'message': "Get is success"}, json_dumps_params={'ensure_ascii': False}, status=200)
        else:
            return JsonResponse({'data': serializedData.errors})

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializedData = BookSerializer(data=data)
        if serializedData.is_valid():
            serializedData.save()
            return JsonResponse({'success': True, 'data': serializedData.data, 'message': "Post is success"}, status=200)
        # 넣으려는 값의 primary_key 값이 이미 db에 존재하는경우
        else:
            return JsonResponse({'success': False, 'data': None, 'message': "Post is failure"}, status=400)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        if Book.objects.get(name=data["name"]) is not None:
            query = Book.objects.get(name=data["name"])
            serializedData = BookSerializer(query, data=data)
            if serializedData.is_valid():
                serializedData.save()
                return JsonResponse({'success': True, 'data': serializedData.data, 'message': "Put is success"}, status=200)
            else:
                return JsonResponse({'success': False, 'data': None, 'message': "Put is failure"}, status=400)
        else:
            return JsonResponse({'success': False, 'data': None, 'message': "The data does not exist"}, status=404)

    elif request.method == "DELETE":
        # 데이터가 비어있어도 정상작동함.
        data = Book.objects.all()
        data.delete()
        return JsonResponse({"success": True, "message": "Delete is success"}, status=200)


@api_view(["DELETE", "GET"])
def aResource(request, primary_key):
    if request.method == "GET":
        # 데이터를 단일로 가져오는경우 get으로 가져온데이터를 대괄호로 묶어줘야함.
        # 단, filter를 사용하면 상관없음.
        # data = [Book.objects.get(pk=primary_key)]
        data = Book.objects.filter(pk=primary_key)
        serializedData = BookSerializer(data=data, many=True)
        if serializedData.is_valid(raise_exception=True):
            # serializedData.data의 타입은 OrderedDict
            return JsonResponse({"data": serializedData.data, "message": "Get is success"}, json_dumps_params={'ensure_ascii': False}, status=200)

    elif request.method == "DELETE":
        # 찾는 데이터가 없을경우를 위한 예외처리
        try:
            data = Book.objects.get(pk=primary_key)
            data.delete()
        except Book.DoesNotExist:
            return JsonResponse({"success": False, "message": "The data does not exist"}, status=404)
        return JsonResponse({"success": True, "message": "Delete is success"}, status=200)
