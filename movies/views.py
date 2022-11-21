from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Genre, People, Movie
from books.models import Book, Card


# Create your views here.
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie' : movie,
    }
    return render(request, 'movies/detail.html', context)

def detail_person(request, person_pk):
    person = get_object_or_404(People, pk=person_pk)
    movies = person.movie_set.all()
    context = {
        'person' : person,
        'movies' : movies,
    }
    return render(request, 'movies/detail_person.html', context)

def recommended(request):
    movies = Movie.objects.all()
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/recommended.html', context)

def search(request):
    searched = request.GET['nav-search-form'].strip()
    movies = Movie.objects.filter(title__contains=searched)
    people = People.objects.filter(name__contains=searched)
    genres = Genre.objects.filter(name__contains=searched)
    genres_movies = []
    for genre in genres:
        genres_movies.extend(genre.movie_set.all())
    books = Book.objects.filter(title__contains=searched)
    context = {
            'searched' : searched,
            'movies' : movies,
            'people' : people,
            'genres' : genres,
            'genres_movies' : genres_movies,
            'books' : books,
        }
    return render(request, 'movies/search.html', context)

def search_book(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    books = Book.objects.filter(user=request.user)
    context = {
        'books' : books,
        'movie' : movie,
    }
    return render(request, 'movies/search_book.html', context)