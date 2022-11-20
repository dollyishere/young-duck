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


def recommended(request):
    movies = Movie.objects.all()
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/recommended.html', context)


def search_book(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # if request.method == 'POST':
    books = Book.objects.filter(user=request.user)
    context = {
        'books' : books,
        'movie' : movie,
    }
    return render(request, 'movies/search_book.html', context)
    # else:
    #     return redirect('movies:search_book')