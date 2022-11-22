from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse
from .forms import BookForm, CardForm
from .models import Book, Card
from movies.models import Genre, Movie, People
import qrcode

# Create your views here.
# signup, login 외 모든 기능은 로그인 후 접근할 수 있으므로, 만약 해당 유저가 login 상태가 아닐 시 login 페이지로 이동하도록 조치함(is_authenticated)

@require_GET
def index(request):
    # 만약 로그인하지 않았을 시, 홈에는 접근 불가
    if request.user.is_authenticated:
        books = Book.objects.filter(user=request.user)
        context = {
            'books' : books,
        }
        return render(request, 'books/index.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save(commit=False)
                book.user = request.user
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
        book = get_object_or_404(Book, pk=book_pk)
        if request.user == book.user:
            book.delete()
            return redirect('books:index')
        else:
            return redirect('books:detail', book.pk)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def create_card(request, book_pk, movie_pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=book_pk)
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.method == 'POST':
            cards = Card.objects.filter(user=request.user)
            if len(cards):
                for card in cards:
                    if movie == card.watched_movie:
                        card.belonged_book.add(book_pk)
                        return redirect('books:detail_card', card.pk)
            form = CardForm(request.POST)
            if form.is_valid():
                card = form.save(commit=False)
                card.user = request.user
                card.watched_movie = movie
                card.save()
                card.belonged_book.add(book_pk)
                if movie.video:
                    qr_img_url = qrcode.make('https://www.youtube.com/watch?v={}'.format(movie.video))
                    print(type(qr_img_url))
                    qr_img_url.save('media/movies/video/{}.png'.format(movie.pk))
                return redirect('books:detail_card', card.pk)
        else:
            form = CardForm()
        context = {
            'form' : form,
            'book' : book,
            'movie' : movie,
        }
        return render(request, 'books/create_card.html', context)
    else:
        return redirect('accounts:login')


@require_GET
def detail_card(request, card_pk):
    if request.user.is_authenticated:
        card = get_object_or_404(Card, pk=card_pk)
        movie = get_object_or_404(Movie, pk=card.watched_movie.pk)
        qr_img = False
        if movie.video:
            qr_img = 'media/movies/video/{}.png'.format(movie.pk)
        context = {
            'card' : card,
            'qr_img' : qr_img,
        }
        return render(request, 'books/detail_card.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def update_card(request, card_pk):
    if request.user.is_authenticated:
        card = get_object_or_404(Card, pk=card_pk)
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
        context = {
            'card' : card,
            'form' : form,
        }
        return render(request, 'books/update_card.html', context)
    else:
        return redirect('accounts:login')


@require_POST
def delete_card(request, card_pk):
    if request.user.is_authenticated:
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
        book = get_object_or_404(Book, pk=book_pk)
        if request.method == 'POST':
            searched = request.POST['searched']
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
