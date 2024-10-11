from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache  # Import cache
from rest_framework import generics, viewsets
from .models import User, Book
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from book.serializers import BookSerializer
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        cache_key = 'user_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            queryset = User.objects.all()
            cache.set(cache_key, queryset, timeout=60 * 3)
            return queryset
        return cached_data

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # Invalidate the cache on user creation
            cache.delete('user_list')
            return CreateUserSerializer
        return UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f'user_detail_{pk}'
        cached_data = cache.get(cache_key)
        if not cached_data:
            response = super().retrieve(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 3)
            return response
        return Response(cached_data)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Invalidate cache after update
        pk = self.kwargs.get('pk')
        cache.delete(f'user_detail_{pk}')

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        # Invalidate cache after deletion
        pk = self.kwargs.get('pk')
        cache.delete(f'user_detail_{pk}')
        cache.delete('user_list')

# User Profile View with caching
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        cache_key = f'user_profile_{user_id}'
        cached_data = cache.get(cache_key)
        if not cached_data:
            user = self.request.user
            cache.set(cache_key, user, timeout=60 * 3)
            return user
        return cached_data

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Invalidate profile cache after update
        user_id = self.request.user.id
        cache.delete(f'user_profile_{user_id}')


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
