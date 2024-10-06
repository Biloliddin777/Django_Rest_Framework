from django.db import models

from book.models import User


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title