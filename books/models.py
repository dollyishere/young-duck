from django.db import models
from django.conf import settings
from movies.models import Movie
import random

# Create your models here.

# cover_image 저장 루트 지정
def cover_image_path(instance, filename):
    return 'images/{}/cover_img/{}'.format(instance.user.username, filename)

class Book(models.Model):
    title = models.CharField(max_length=20)
    semi_title = models.CharField(max_length=50)
    cover_image = models.ImageField(
        blank=True,
        upload_to=cover_image_path,
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_books')

class Card(models.Model):
    my_score = models.FloatField()
    my_comment = models.TextField()
    visited_count = models.IntegerField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    watched_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cards')
    belonged_book = models.ManyToManyField(Book, related_name='collected_cards')
    