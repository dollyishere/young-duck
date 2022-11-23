from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Genre, People, Movie
from books.models import Book, Card
import random

# Create your views here.
# signup, login 외 모든 기능은 로그인 후 접근할 수 있으므로, 만약 해당 유저가 login 상태가 아닐 시 login 페이지로 이동하도록 조치함(is_authenticated)

@require_GET
def detail(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        movie.click_count += 1
        movie.save()
        movie.refresh_from_db

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
        genre_list = []
        genres = Genre.objects.all()
        for genre in genres:
            genre_list.append(genre)
        choice_genres = random.sample(genre_list, 3)
        # for choice_genre in choice_genres:
        #     print(choice_genre.name)
        #     '{}'.format() = choice_genre.movie_set.all()[:10] 
            # '{}'.format(choice_genre[i]) = Genre.movie_set.filter
        
        movies = Movie.objects.all()
        longest_title = ''
        longest_overview = ''
        longest_name = ''
        longest_director_name = ''

        for movie in movies:
            if len(movie.title) > len(longest_title):
                longest_title = movie.title
            if len(movie.overview) > len(longest_overview):
                longest_overview = movie.overview
            if len(movie.director) > len(longest_director_name):
                longest_director_name = movie.director

        people = People.objects.all()
        
        for person in people:
            if len(person.name) > len(longest_name):
                longest_name = person.name
        
        print(longest_title)
        print(longest_overview)
        print(longest_name)
        print(longest_director_name)

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
        movies = Movie.objects.filter(title__contains=searched).order_by('-popularity')
        people = People.objects.filter(name__contains=searched).order_by('-popularity')
        genres = Genre.objects.filter(name__contains=searched)
        genres_movies = []
        for genre in genres:
            genres_movies.extend(genre.movie_set.all())
        genres_movies.sort(key=lambda x:x.popularity, reverse=True)
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