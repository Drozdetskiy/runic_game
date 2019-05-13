from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Link(models.Model):
    link = models.CharField(max_length=100)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Game(models.Model):
    link_1 = models.ForeignKey('api.Link', related_name='link_1', on_delete=models.CASCADE)
    link_2 = models.ForeignKey('api.Link', related_name='link_2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
