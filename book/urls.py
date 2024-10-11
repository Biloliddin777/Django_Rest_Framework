from django.urls import path

from .views import UserListCreateView, UserDetailView, UserProfileView
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet

router = DefaultRouter()
router.register(r'my_book_list', BookViewSet, basename='book')
urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]

urlpatterns += router.urls
