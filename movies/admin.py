from django.contrib import admin
from .models import Genre, People, Movie
# Register your models here.

admin.site.register(Genre)
admin.site.register(People)
admin.site.register(Movie)