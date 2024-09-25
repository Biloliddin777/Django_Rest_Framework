from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from olcha.models import Product, Image, Comment
from olcha.serializers import ProductSerializer, ImageSerializer, CommentSerializer


class ProductListApiView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageListApiView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class CommentListApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
