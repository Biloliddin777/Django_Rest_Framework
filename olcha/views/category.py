from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from olcha.models import Category, Group
from olcha.serializers import CategorySerializer, GroupSerializer


class CategoryDetailApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_slug):
        cache_key = f'category_detail_{category_slug}'
        cached_data = cache.get(cache_key)

        if not cached_data:
            try:
                category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CategorySerializer(category, context={'request': request})
            cache.set(cache_key, serializer.data, timeout=60 * 3)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(cached_data, status=status.HTTP_200_OK)


class CategoryListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = 'category_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            cache.set(cache_key, serializer.data, timeout=60 * 3)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(cached_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('category_list')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
