from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from rest_framework.authtoken import views
from debug_toolbar.toolbar import debug_toolbar_urls


from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('book/', include('book.urls')),
                  path('api-auth/', include('rest_framework.urls')),
                  path('olcha/', include('olcha.urls')),
                  path('api-token-auth/', views.obtain_auth_token),
                  path('user/', include('user.urls')),
                  path('post/', include('post.urls')),

                  path('api/token/access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += debug_toolbar_urls()