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
    # 영화 detail의 경우, 먼저 movie_pk를 통해 해당하는 영화를 불러옵니다.
    # 이후 click_count를 자동으로 1 증가시킨 후 save()하게 합니다(이후 영화 추천에 반영됨).
    # 정보를 최신 기준으로 변경해줍니다(refresh_from_db).
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        movie.click_count += 1
        movie.save()
        movie.refresh_from_db

        # 해당 영화에 출연한 인물과 해당 영화의 장르에 대한 정보를 각각 역참조로 불러옵니다(N:M).
        # people의 경우 인지도가 높은 순으로 정렬합니다.
        people = movie.people.all().order_by('-popularity')
        genres = movie.genres.all()
        
        # 해당 영화에 출연한 인물의 경우, 만약 5명이 넘어가면 5명의 데이터만 조회하도록 설정합니다.
        if len(people) >= 5:
            people = people[:5]
        
        # 해당 영화를 토대로 만들어진 cards의 정보를 역참조를 통해 모두 불러옵니다.
        # 그리고 해당 영화가 속한 books의 정보를 모두 불러온 후, books 리스트에 extend로 추가합니다.
        # 이후 books 내부 데이터를 sort를 통해 가장 최근 업데이트 된 순으로 정렬합니다.
        cards = movie.cards.all()
        books = []

        for card in cards:
            books_list = card.belonged_book.all()
            books.extend(books_list)
        
        books.sort(key=lambda x:x.updated_at, reverse=True)
        
        # 해당 페이지에 접속한 유저가 만든 테마북 정보들을 가져옵니다.
        my_books = Book.objects.filter(user=request.user)

        context = {
            'movie' : movie,
            'people' : people,
            'genres' : genres,
            'books' : books,
            'my_books' : my_books,
        }
        return render(request, 'movies/detail.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def detail_person(request, person_pk):
    if request.user.is_authenticated:
        # 해당하는 인물에 대한 정보를 person_pk를 통해 받아옵니다.
        # 이후 click_count를 자동으로 1 증가시킨 후 save()하게 합니다(이후 영화 추천에 반영됨).
        # 정보를 최신 기준으로 변경해줍니다(refresh_from_db).
        person = get_object_or_404(People, pk=person_pk)
        person.click_count += 1
        person.save()
        person.refresh_from_db

        # 역참조를 사용하여 해당 인물이 출연한 영화 정보를 받아옵니다.
        movies = person.movie_set.all().order_by('-popularity')

        # 만약 출연한 영화의 수가 5 이상이라면, 인덱싱을 진행합니다.
        if len(movies) >= 5:
            movies = movies[:5]
        
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
        # 먼저 장르 이름(name)을 받아 리스트에 담아준 후, random 함수를 이용하여 랜덤으로 세 장르를 선택합니다.
        # 이후 해당 장르 이름을 통해 해당 장르를 가지고 있는 영화들을 받아와 저장해줍니다.
        # 슬라이싱의 경우, recommended에서 직접 진행합니다.
        genre_name_list = []
        genres = Genre.objects.all()
        movies = Movie.objects.all()

        for genre in genres:
            genre_name_list.append(genre)
        choice_genres = random.sample(genre_name_list, 3)


        # popular_people의 경우, 인기도가 높은 순으로 정렬하여 그 중 5명의 데이터만 추려내어 저장합니다.
        popular_people = People.objects.all().order_by('-popularity')[:5]

        # top_clicked_movies의 경우, 클릭 횟수(click_count)가 높았던 순으로 정렬한 후 그 중 5개의 데이터만 추려내어 저장합니다.
        top_clicked_movies = Movie.objects.all().order_by('-click_count')[:5]

        context = {
            'movies' : movies,
            'choice_genres' : choice_genres,
            'popular_people' : popular_people,
            'top_clicked_movies' : top_clicked_movies,
        }
        return render(request, 'movies/recommended.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def search(request):
    if request.user.is_authenticated:
        # 검색창에 입력한 데이터의 경우 request.GET을 통해 받아와 좌우 공백을 제거한 후에 사용합니다.
        # 이후 movies와 people은 인기 순으로 정렬합니다.
        searched = request.GET['nav-search-form'].strip()
        movies = Movie.objects.filter(title__contains=searched).order_by('-popularity')
        people = People.objects.filter(name__contains=searched).order_by('-popularity')
        genres = Genre.objects.filter(name__contains=searched)
        books = Book.objects.filter(title__contains=searched)
        
        # 장르의 경우, 일단 searched 키워드에 맞는 장르를 contains로 대조하여 filter해 구한 후, 역참조로 해당하는 리스트를 불러옵니다.
        # 이후 해당 영화 리스트 내부 데이터를 sort를 사용해 popularity 순으로 정렬합니다.
        genres_movies = []
        for genre in genres:
            genres_movies.extend(genre.movie_set.all())
        genres_movies.sort(key=lambda x:x.popularity, reverse=True)
        
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
        # movie_pk를 사용하여 해당 영화 정보를 불러옵니다.
        # 이후 현재 접속한 유저가 제작한 book의 정보를 filter를 통해 불러옵니다.
        movie = get_object_or_404(Movie, pk=movie_pk)
        books = Book.objects.filter(user=request.user)

        context = {
            'books' : books,
            'movie' : movie,
        }
        return render(request, 'movies/select_book.html', context)
    else:
        return redirect('accounts:login')