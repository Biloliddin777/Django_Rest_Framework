from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from olcha.models import Product, Image, Comment, AttributeKey, AttributeValue, ProductAttribute
from olcha.serializers import ProductSerializer, ImageSerializer, CommentSerializer, AttributeKeySerializer, AttributeValueSerializer, ProductAttributeSerializer


class ProductListApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ImageListApiView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CommentListApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AttributeKeyListApiView(ListCreateAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer


class AttributeValueListApiView(ListCreateAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class ProductAttributeListApiView(ListCreateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
