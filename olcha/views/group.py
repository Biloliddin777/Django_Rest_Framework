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


class GroupList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = 'group_list'
        cached_data = cache.get(cache_key)

        if not cached_data:
            groups = Group.objects.all()
            serializer = GroupSerializer(groups, many=True)
            cache.set(cache_key, serializer.data, timeout=60 * 3)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(cached_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('group_list')
            data = {
                'success': True,
                'message': 'Group created successfully'
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailApiView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return None

    def get(self, request, pk):
        cache_key = f'group_detail_{pk}'
        cached_data = cache.get(cache_key)

        if not cached_data:
            group = self.get_object(pk)
            if group is None:
                return Response(data={'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = GroupSerializer(group)
            cache.set(cache_key, serializer.data, timeout=60 * 3)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(cached_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()

            cache.delete(f'group_detail_{pk}')
            cache.delete('group_list')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_object(pk)
        if group is None:
            return Response(data={'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)

        group.delete()
        cache.delete(f'group_detail_{pk}')
        cache.delete('group_list')
        return Response(data={'status': 'success'}, status=status.HTTP_200_OK)
