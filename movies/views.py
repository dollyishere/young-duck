from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Genre, People, Movie
from books.models import Book, Card


# Create your views here.
# signup, login 외 모든 기능은 로그인 후 접근할 수 있으므로, 만약 해당 유저가 login 상태가 아닐 시 login 페이지로 이동하도록 조치함(is_authenticated)

@require_GET
def detail(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        people = movie.people.all()
        genres = movie.genres.all()
        
        if len(people) >= 5:
            people = people[:5]
        
        context = {
            'movie' : movie,
            'people' : people,
            'genres' : genres,
        }
        return render(request, 'movies/detail.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def detail_person(request, person_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(People, pk=person_pk)
        movies = person.movie_set.all()
        context = {
            'person' : person,
            'movies' : movies,
        }
        return render(request, 'movies/detail_person.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def recommended(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all()
        context = {
            'movies' : movies,
        }
        return render(request, 'movies/recommended.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def search(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('accounts:login')


@require_GET
def select_book(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        books = Book.objects.filter(user=request.user)
        context = {
            'books' : books,
            'movie' : movie,
        }
        return render(request, 'movies/select_book.html', context)
    else:
        return redirect('accounts:login')