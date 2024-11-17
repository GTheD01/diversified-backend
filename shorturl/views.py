import string
import random
import re

from functools import wraps
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shorturl.serializers import ShortUrlSerializer
from shorturl.models import ShortUrl

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


# Rate Limit for Short urls
# Used just in case user posting/creating short urls to prevent malicious attacks/brute force
def ratelimit_post(rate_limit, time_window):
    def decorator(view_func): # View func refers to the function we want to wrap in this case (shortUrl)
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                ip_address = request.META.get('REMOTE_ADDR')
                cache_key = f'ratelimit:{ip_address}'
                request_count = cache.get(cache_key, 0)
                if request_count >= rate_limit:
                    return Response({'error': 'Rate limit exceeded'}, status=429)
                cache.set(cache_key, request_count + 1, time_window)
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

# Short url endpoints
@ratelimit_post(rate_limit=2, time_window=100)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
            return Response({'error':"Url not valid, url example: http://www...."}, status=status.HTTP_400_BAD_REQUEST)
        shortened_url = ShortUrl.objects.create(
            original_url = original_url,
            short_url = short_url,
            created_by = request.user
        )
        serializer = ShortUrlSerializer(shortened_url, many=False)
        return Response(serializer.data)

# THE CODE BELOW SHOULD BE CHANGED
@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticated])
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