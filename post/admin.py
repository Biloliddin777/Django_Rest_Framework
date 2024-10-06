from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from post.models import Post

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = Post
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Post)