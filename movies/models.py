from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

class People(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True)
    known_for_department = models.CharField(max_length=50)
    popularity = models.FloatField()
    profile_path = models.CharField(max_length=200, blank=True)
    # click_count = models.IntegerField()

class Movie(models.Model):
    title = models.CharField(max_length=100)
    released_date = models.DateField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    homepage = models.CharField(max_length=100, blank=True)
    runtime = models.IntegerField()
    status = models.CharField(max_length=50, blank=True)
    overview = models.TextField()
    poster_path = models.CharField(max_length=200, blank=True)
    backdrop_path = models.CharField(max_length=200, blank=True)
    budget = models.IntegerField()
    video = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=100)
    click_count = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    people = models.ManyToManyField(People, blank=True)
    