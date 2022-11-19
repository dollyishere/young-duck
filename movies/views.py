from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Genre, People, Movie


# Create your views here.
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie' : movie,
    }
    return render(request, 'movies/detail.html', context)


def recommended(request):
    movies = Movie.objects.all()
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/recommended.html', context)