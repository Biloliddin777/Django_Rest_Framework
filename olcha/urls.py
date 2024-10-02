from django.urls import path
from olcha.views import category, group, product
from olcha.views.product import (
    AttributeKeyListApiView,
    AttributeValueListApiView,
    ProductAttributeListApiView
)

urlpatterns = [
    path('categories/', category.CategoryListApiView.as_view(), name='categories'),
    path('groups/', group.GroupList.as_view(), name='groups'),
    path('category/<slug:slug>/', category.CategoryDetailApiView.as_view(), name='category'),
    path('groups/detail/<int:pk>/', group.GroupDetailApiView.as_view()),
    path('all-products/', product.ProductListApiView.as_view(), name='all-products'),
    path('all-images/', product.ImageListApiView.as_view(), name='all-products'),
    path('all-comments/', product.CommentListApiView.as_view(), name='all-comments'),

    # Attributes
    path('attribute-keys/', AttributeKeyListApiView.as_view(), name='attribute-keys'),
    path('attribute-values/', AttributeValueListApiView.as_view(), name='attribute-values'),
    path('product-attributes/', ProductAttributeListApiView.as_view(), name='product-attributes'),
]
