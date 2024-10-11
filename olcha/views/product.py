from django.core.cache import cache
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from olcha.models import Product, Image, Comment, AttributeKey, AttributeValue, ProductAttribute
from olcha.serializers import ProductSerializer, ImageSerializer, CommentSerializer, AttributeKeySerializer, \
    AttributeValueSerializer, ProductAttributeSerializer


class ProductListApiView(ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'product_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 3)
            return response

        return Response(cached_data, status=status.HTTP_200_OK)


class ImageListApiView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'image_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 3)
            return response

        return Response(cached_data, status=status.HTTP_200_OK)


class CommentListApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'comment_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 3)
            return response

        return Response(cached_data, status=status.HTTP_200_OK)


class AttributeKeyListApiView(ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'attribute_key_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 3)
            return response

        return Response(cached_data, status=status.HTTP_200_OK)


class AttributeValueListApiView(ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'attribute_value_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 3)
            return response

        return Response(cached_data, status=status.HTTP_200_OK)


class ProductAttributeListApiView(ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'product_attribute_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 3)
            return response

        return Response(cached_data, status=status.HTTP_200_OK)
