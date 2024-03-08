import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task, Expense, ShortUrl
from .serializers import AvatarSerializer, TaskSerializer, ExpenseSerializer, ShortUrlSerializer
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

import string
import random
import re




class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        response.delete_cookie(key='access', samesite='none')
        response.delete_cookie(key='refresh', samesite='none')

        return response
    

# Upload avatar endpoint
class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if request.user.avatar:
            request.user.avatar.delete()

        serializer = AvatarSerializer(instance=request.user, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=500)
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            user.avatar.delete()
            # Delete associated folder if empty
            pk_folder_path = os.path.abspath(os.path.join(os.getcwd(), 'media' , 'images', 'avatars', str(user.pk)))
            if os.path.exists(pk_folder_path) and not os.listdir(pk_folder_path):
                os.rmdir(pk_folder_path)
            return Response({'message': 'Avatar deleted successfully'})
        except Exception as e:
            return Response({'message': str(e)}, status=500)


# Tasks endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks(request):
    if request.method == 'GET':
        user = request.user
        tasks = user.task_set.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        task = Task.objects.create(
            label = request.data['label'],
            description = request.data['description'],
            created_by = request.user
        )
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "PUT":
        task.label = request.data['label']
        task.description = request.data['description']
        task.save()

        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)
    
    if request.method == "DELETE":
        task.delete()
        return Response("Task deleted")

# Expenses endpoints
@api_view(['GET', 'POST'])
def expenses(request):
    if request.method == "GET":
        user = request.user
        expenses = user.expense_set.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        expense = Expense.objects.create(
            label = request.data['label'],
            price = request.data['price'],
            created_by = request.user
        )
        serializer = ExpenseSerializer(expense, many=False)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def expense(request, id):
    expense = Expense.objects.get(pk=id)
    if request.method == "PUT":
        expense.label = request.data['label']
        expense.price = request.data['price']
        expense.save()

        serializer = ExpenseSerializer(expense, many=False)
        return Response(serializer.data)
    
    if request.method == "DELETE":
        expense.delete()
        return Response("Expense deleted")
    

# URL validation regex
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


# Generate short url
def generate_short_url():
    chars = list(string.ascii_letters)
    random_chars = ''
    for i in range(6):
        random_chars += random.choice(chars)
    while len(ShortUrl.objects.filter(short_url=random_chars)) != 0:
        for i in range(6):
            random_chars += random.choice(chars)
    return random_chars

# Short url endpoints
@api_view(['GET', 'POST'])
def shortUrl(request):
    if request.method == 'GET':
        user = request.user
        shortened_urls = user.shorturl_set.all()
        serializer = ShortUrlSerializer(shortened_urls, many=True)
        return Response(serializer.data)
    

    if request.method == "POST":
        short_url = generate_short_url()
        original_url = request.data['original_url']
        match = re.match(regex, original_url) is not None
        if not match:
            return Response("Url not valid, url example: http://www....")
        shortened_url = ShortUrl.objects.create(
            original_url = original_url,
            short_url = short_url,
            created_by = request.user
        )
        serializer = ShortUrlSerializer(shortened_url, many=False)
        return Response(serializer.data)

@api_view(['DELETE', 'GET'])
def shortUrlDel(request, id):
    # Using id as a number/integer to delete practicular short url
    if request.method == "DELETE":
        short_url = ShortUrl.objects.get(pk=id)
        short_url.delete()
        return Response('Short Url deleted')
    
    # the id type is different depending on the request method 
    # so that on frontend its easier to retrieve some informations
    
    # Using id as string to pass short url params from the frontend
    # to get the original url from backend, so we can redirect on the frontend
    if request.method == 'GET':
        short_url = ShortUrl.objects.get(short_url=id)
        serializer = ShortUrlSerializer(short_url, many=False)
        return Response(serializer.data['original_url'])