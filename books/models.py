from django.db import models
from django.conf import settings
from movies.models import Movie

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=20)
    semi_title = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Card(models.Model):
    my_score = models.IntegerField()
    my_comment = models.TextField()
    visits_count = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    belonged_book = models.ManyToManyField(Book, related_name='card')
    movie = models.ManyToManyField(Movie, related_name='card')