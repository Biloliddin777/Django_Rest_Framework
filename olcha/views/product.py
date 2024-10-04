from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from olcha.models import Product, Image, Comment, AttributeKey, AttributeValue, ProductAttribute
from olcha.serializers import ProductSerializer, ImageSerializer, CommentSerializer, AttributeKeySerializer, \
    AttributeValueSerializer, ProductAttributeSerializer


class ProductListApiView(ListCreateAPIView):
    permission_classes = [AllowAny, ]
    # authentication_classes = [JWTAuthentication, ]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageListApiView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CommentListApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AttributeKeyListApiView(ListCreateAPIView):
    permission_classes = [AllowAny]
    # authentication_classes = [JWTAuthentication]
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer


class AttributeValueListApiView(ListCreateAPIView):
    permission_classes = [AllowAny]
    # authentication_classes = [JWTAuthentication]
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class ProductAttributeListApiView(ListCreateAPIView):
    permission_classes = [AllowAny]
    # authentication_classes = [JWTAuthentication]
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
