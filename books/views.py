from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse
from .forms import BookForm, CardForm
from .models import Book, Card
from movies.models import Genre, Movie, People
import qrcode
import random

# 이하는 colorthief 기동을 위해 필요한 라이브러리 import 코드임을 밝힙니다.
import sys

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import io

from colorthief import ColorThief

# Create your views here.
# signup, login 외 모든 기능은 로그인 후 접근할 수 있으므로, 만약 해당 유저가 login 상태가 아닐 시 login 페이지로 이동하도록 조치함(is_authenticated)

@require_GET
def index(request):
    # 만약 로그인하지 않았을 시, 홈에는 접근 불가
    if request.user.is_authenticated:
        # 메인 화면에서는 유저 자신이 제작한 테마북을 확인할 수 있습니다.
        # filter를 이용해 현재 요청한 사용자가 제작한 테마북 정보를 모두 불러옵니다.
        books = Book.objects.filter(user=request.user)

        # 추천 테마북을 like_user순으로 구해옵니다.
        # https://www.reddit.com/r/learnpython/comments/71v8jo/django_order_queryset_by_a_manytomanyfieldcount/ 참조
        popular_books = Book.objects.all()\
            .annotate(num_likes=Count('like_users'))\
                .order_by('-num_likes')
        
        # 만약 친구가 존재한다면, 친구 정보와 해당 친구들의 테마북 데이터를 불러와 friends_books에 저장한 후, -pk 순으로 sort를 통해 정렬합니다.
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        friends = user.followings.all()
        friends_books = []

        if friends:
            for friend in friends:
                friend_books = friend.book_set.all().order_by('-pk')
                friends_books.extend(friend_books)

            friends_books.sort(key=lambda x:x.pk, reverse=True)

        context = {
            'books' : books,
            'popular_books' : popular_books,
            'friends' : friends,
            'friends_books' : friends_books,
        }
        return render(request, 'books/index.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.user.is_authenticated:
        # 만약 POST로 접근하였고, request.POST로 전달된 정보들을 넣은 form이 valid하다면, 신규 테마북을 생성합니다.
        # 사용자가 cover_image를 설정하지 않았다면, 기존에 'media/images/cover_img/' 폴더에 저장되어 있던 50 장의 이미지 중 랜덤으로 하나를 선정하여 경로값을 넣어줍니다.
        # 만약 GET으로 접근하였다면, 테마북 제작 화면으로 이동합니다.
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save(commit=False)
                book.user = request.user
                if book.cover_image == '':
                    book.cover_image = 'images/cover_img/{}.jpg'.format(random.randrange(1, 51))
                book.save()
                return redirect('books:detail', book.pk)
        else:
            form = BookForm()
        context = {
            'form' : form,
        }
        return render(request, 'books/create.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def detail(request, book_pk):
    if request.user.is_authenticated:
        # 테마북 상세 조회 페이지에서는 해당 테마북 정보, 해당 테마북을 제작한 인물에 대한 정보, 해당 테마북에 속한 카드 정보를 불러와 context에 저장합니다.
        # 이후 render 시 해당 정보를 html 측으로 전달합니다.
        book = get_object_or_404(Book, pk=book_pk)
        person = get_object_or_404(get_user_model(), pk=book.user.pk)
        cards = book.collected_cards.all()

        context = {
            'book' : book,
            'person' : person,
            'cards' : cards,
        }
        return render(request, 'books/detail.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def update(request, book_pk):
    if request.user.is_authenticated:
        # 테마북 정보 수정을 진행하는 함수입니다.
        # 먼저 book_pk로 해당 테마북에 대한 정보를 불러옵니다.
        # if문을 사용해 해당 테마북을 제작한 유저와 현재 요청한 사용자가 같다면, 수정이 가능하게 합니다.
        # 만약 접근 방법이 POST이고, request.POST를 통해 불러온 정보를 넣은 form이 valid하다면, 업데이트를 진행합니다.
        # 만약 접근 방법이 GET이라면, 테마북 수정 페이지로 이동합니다.
        book = get_object_or_404(Book, pk=book_pk)
        if request.user == book.user:
            if request.method == 'POST':
                form = BookForm(request.POST, request.FILES, instance=book)
                if form.is_valid():
                    form.save()
                    return redirect('books:detail', book.pk)
            else:
                form = BookForm(instance=book)
        else:
            return redirect('books:detail', book.pk)
        context = {
            'book' : book,
            'form' : form,
        }
        return render(request, 'books/update.html', context)
    else:
        return redirect('accounts:login')


@require_POST
def delete(request, book_pk):
    if request.user.is_authenticated:
        # 테마북 삭제를 진행합니다.
        # 만약 테마북을 제작한 유저와 현재 삭제를 요청한 사용자가 일치한다면, 삭제를 진행합니다.
        book = get_object_or_404(Book, pk=book_pk)
        if request.user == book.user:
            book.delete()
            return redirect('books:index')
        else:
            return redirect('books:detail', book.pk)
    else:
        return redirect('accounts:login')


# 좋아하는 테마북에 좋아요를 누를 수 있습니다.
# 비동기로 구현했습니다.
@require_POST
def like(request, book_pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=book_pk)
        is_liked = False
        if book.like_users.filter(pk=request.user.pk).exists():
            is_liked = False
            book.like_users.remove(request.user)
        else:
            is_liked = True
            book.like_users.add(request.user)
        context = {
            'is_liked' : is_liked,
            'like_count' : book.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')

@require_http_methods(['GET', 'POST'])
def create_card(request, book_pk, movie_pk):
    if request.user.is_authenticated:
        # 카드를 제작하는 함수입니다.
        # 먼저 book_pk와 movie_pk를 이용해 해당하는 테마북과 영화에 대한 정보를 각각 받아옵니다.
        # 이후 해당 영화의 장르들과 해당 영화 제작에 참여한 인물에 대한 정보를 역참조로 받아옵니다.
        book = get_object_or_404(Book, pk=book_pk)
        movie = get_object_or_404(Movie, pk=movie_pk)
        genres = movie.genres.all()
        people = movie.people.all()

        # 만약 장르와 인물의 수가 5개(명)보다 많다면, 인덱싱을 진행합니다.
        if len(people) >= 5:
            people = people[:5]

        if len(genres) >= 5:
            genres = genres[:5]
            
        # 만약 접근 방법이 POST라면, 카드 제작을 진행합니다.
        # 먼저 해당 유저가 제작한 카드들에 대한 정보를 filter를 통해 전부 불러옵니다.
        # 만약 cards의 수가 1 이상이라면, for문을 통해 각 카드 정보를 조회합니다.
        # 만약 해당 카드와 연결된 movie가 현재 선택한 movie라면, belonged_book에 해당 테마북의 pk를 추가한 후, 해당 테마북 상세 페이지로 리다이렉트합니다.
        if request.method == 'POST':
            cards = Card.objects.filter(user=request.user)
            if cards:
                for card in cards:
                    if movie == card.watched_movie:
                        if book in card.belonged_book.all():
                            card.belonged_book.remove(book_pk)
                            return redirect('books:index')
                        else:
                            card.belonged_book.add(book_pk)
                            return redirect('books:detail', book_pk)

        # 만약 신규로 생성되는 카드라면, 카드를 신규 생성합니다.
        # 이때 만약 해당 movie의 video field에 값이 존재한다면, qrcode 라이브러리로 qrcode를 생성한 후 'media/movies/video/' 파일에 저장합니다.
        # 이후 해당 테마북 상세 페이지로 리다이렉트합니다.
            form = CardForm(request.POST)

            if form.is_valid():
                card = form.save(commit=False)
                card.user = request.user
                card.watched_movie = movie

                # 만약 사용자가 디폴트 값을 입력하지 않았을 시, 디폴트 값을 입력
                if card.visited_count == None:
                    card.visited_count = 0

                card.save()
                card.belonged_book.add(book_pk)
                if movie.video:
                    qr_img_url = qrcode.make('https://www.youtube.com/watch?v={}'.format(movie.video))
                    print(type(qr_img_url))
                    qr_img_url.save('media/movies/video/{}.png'.format(movie.pk))
                return redirect('books:detail', book_pk)
        else:
            form = CardForm()
            form.fields['visited_count'].initial = 0

        # 만약 GET로 접근했다면, 카드 생성 페이지로 이동합니다.
        # 이때 colorthief 라이브러리를 이용하여, 해당 영화의 backdrop 이미지의 컬러 팔레트를 추출해냅니다.
        # 그리고 해당 컬러 팔레트에서 3번째로 점유율이 높은 색을 선택하여 해당 색을 각각 r, g, b로 나누어 context에 저장합니다.
        # 이후 해당 정보들을 카드 배경을 만들 때 사용합니다.
        fd = urlopen('https://image.tmdb.org/t/p/w500{}'.format(movie.backdrop_path))
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        dominant_color = color_thief.get_palette(color_count=3)[2]
        dominant_color = list(dominant_color)

        context = {
            'form' : form,
            'book' : book,
            'movie' : movie,
            'genre' : genres,
            'people' : people,
            'r' : dominant_color[0],
            'g' : dominant_color[1],
            'b' : dominant_color[2],
        }
        return render(request, 'books/create_card.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def detail_card(request, card_pk):
    if request.user.is_authenticated:
        # 카드 상세 페이지입니다.
        # 전체적인 로직은 테마북 상세 페이지와 비슷합니다.
        card = get_object_or_404(Card, pk=card_pk)
        movie = get_object_or_404(Movie, pk=card.watched_movie.pk)
        genres = movie.genres.all()
        people = movie.people.all()

        if len(people) >= 5:
            people = people[:5]

        if len(genres) >= 5:
            genres = genres[:5]
        
        # 만약 movie video 정보가 존재한다면, qr_img에 해당 qrcode 이미지가 존재하는 경로 값을 저장합니다.
        qr_img = False
        if movie.video:
            qr_img = 'media/movies/video/{}.png'.format(movie.pk)

        # 여기서도 colorthief를 사용합니다.
        fd = urlopen('https://image.tmdb.org/t/p/w500{}'.format(movie.backdrop_path))
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        dominant_color = color_thief.get_palette(color_count=3)[2]
        dominant_color = list(dominant_color)

        context = {
            'card' : card,
            'movie' : movie,
            'qr_img' : qr_img,
            'genre' : genres,
            'people' : people,
            'r' : dominant_color[0],
            'g' : dominant_color[1],
            'b' : dominant_color[2],
        }
        return render(request, 'books/detail_card.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def update_card(request, card_pk):
    if request.user.is_authenticated:
        # 카드 업데이트를 진행합니다.
        # 전체적인 로직은 카드 생성 페이지와 비슷합니다.
        card = get_object_or_404(Card, pk=card_pk)
        movie = get_object_or_404(Movie, pk=card.watched_movie.pk)
        genres = movie.genres.all()
        people = movie.people.all()

        if len(people) >= 5:
            people = people[:5]

        if len(genres) >= 5:
            genres = genres[:5]

        # 만약 접근 방식이 POST이고, request.POST를 통해 불러온 정보를 저장한 form이 valid하다면, 카드를 업데이트합니다.
        # 만약 접근 방식이 GET이라면, 카드 수정 페이지로 이동합니다.
        if request.user == card.user:
            if request.method == 'POST':
                form = CardForm(request.POST, instance=card)
                if form.is_valid():
                    form.save()
                    return redirect('books:detail_card', card.pk)
            else:
                form = CardForm(instance=card)
        else:
            return redirect('books:detail_card', card.pk)

        # 여기서도 colorthief를 사용합니다.
        fd = urlopen('https://image.tmdb.org/t/p/w500{}'.format(movie.backdrop_path))
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        dominant_color = color_thief.get_palette(color_count=3)[2]
        dominant_color = list(dominant_color)

        context = {
            'card' : card,
            'form' : form,
            'movie' : movie,
            'genre' : genres,
            'people' : people,
            'r' : dominant_color[0],
            'g' : dominant_color[1],
            'b' : dominant_color[2],
        }
        return render(request, 'books/update_card.html', context)
    else:
        return redirect('accounts:login')

@require_POST
def delete_card(request, card_pk):
    if request.user.is_authenticated:
        # 카드를 삭제합니다.
        # 만약 카드를 제작했던 유저와 현재 삭제를 요청하는 유저가 같다면, 카드를 삭제합니다.
        card = get_object_or_404(Book, pk=card_pk)
        if request.user == card.user:
            card.delete()
            return redirect('books:index')
        else:
            return redirect('books:detail_card', card.pk)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def select_movie(request, book_pk):
    if request.user.is_authenticated:
        # 먼저 book_pk를 이용해 카드를 만들고자 하는 테마북의 정보를 받아옵니다.
        book = get_object_or_404(Book, pk=book_pk)
        
        # 만약 POST로 접근했다면, 영화 검색을 진행합니다.
        # 검색창에 입력한 단어를 strip()을 통해 공백을 삭제해준 후, 해당 정보가 담긴 영화, 인물, 장르들에 대한 정보를 filter를 통해 가져옵니다.
        # 만약 GET으로 접근했다면, 영화 검색 및 선택 페이지로 이동합니다.
        if request.method == 'POST':
            searched = request.POST['searched'].strip()
            movies = Movie.objects.filter(title__contains=searched)
            people = People.objects.filter(name__contains=searched)
            genres = Genre.objects.filter(name__contains=searched)
            context = {
                'searched' : searched,
                'movies' : movies,
                'people' : people,
                'genres' : genres,
                'book' : book,
            }
        else:
            context = {
                'book' : book,
            }
        return render(request, 'books/select_movie.html', context)
    else:
        return redirect('accounts:login')


@require_POST
def steal_book(request, book_pk):
    if request.user.is_authenticated:
        # 다른 유저 또는 해당 유저가 제작한 테마북과 그 하위 카드들의 정보를 가져와 새로 자신의 테마북으로 만듭니다.
        # 만약 이미 제작한 영화 카드라면 해당 카드의 belonged_book에 해당 테마북 정보를 새로 넣어줍니다.
        # 만약 제작된 적 없는 영화 카드라면 기본값을 모두 0, ''으로 지정한 후 해당 테마북과 연결해줍니다.
        book = get_object_or_404(Book, pk=book_pk)
        cards = book.collected_cards.all()
        movies = []
        for card in cards:
            your_movie = get_object_or_404(Movie, pk=card.watched_movie.pk)
            movies.append(your_movie)

        book_form = BookForm()
        my_book = book_form.save(commit=False)
        my_book.user = request.user
        my_book.title = book.title
        my_book.semi_title = book.semi_title
        my_book.cover_image = book.cover_image
        my_book.save()

        for movie in movies:
            my_collection = Card.objects.filter(
                watched_movie=movie,
                user=request.user
                )
            print(my_collection)  
            if my_collection:
                my_collection[0].belonged_book.add(my_book.pk)
            else:
                card_form = CardForm()
                my_card = card_form.save(commit=False)
                my_card.user = request.user
                my_card.watched_movie = movie
                my_card.my_score = 0.0
                my_card.my_comment = ''
                my_card.visited_count = 0
                my_card.save()
                
                my_card.belonged_book.add(my_book.pk)

        return redirect('books:detail', my_book.pk)
    else:
        return redirect('accounts:login')
