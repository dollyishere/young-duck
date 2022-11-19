from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from .forms import BookForm, CardForm
from .models import Book, Card
from movies.models import Genre, Movie, People

# Create your views here.
def index(request):
    # 만약 로그인하지 않았을 시, 홈에는 접근 불가
    if request.user.is_authenticated:
        people = get_list_or_404(get_user_model())
        context = {
            'people' : people,
        }
        return render(request, 'books/index.html', context)
    else:
        redirect('accounts:login')


def create(request):
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


def detail(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    context = {
        'book' : book,
    }
    return render(request, 'books/detail.html', context)


def update(request, book_pk):
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


def delete(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.user.is_authenticated:
        if request.user == book.user:
            book.delete()
            return redirect('books:index')
    return redirect('books:detail', book.pk)


def create_card(request, book_pk, movie_pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_pk)
        movie = get_object_or_404(Movie, pk=movie_pk)
        cards = Card.objects.filter(user=request.user)
        if len(cards):
            for card in cards:
                if card.watched_movie == movie:
                    card.belonged_book.add(book.pk)
                    return redirect('books:detail', book.pk)
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.belonged_book = book
            card.watched_movie = movie
            card.save()
            return redirect('books:detail_card', card.pk)
    else:
        form = CardForm()
    context = {
        'form' : form,
        'book' : book,
        'movie' : movie,
    }
    return render(request, 'books/create_card.html', context)


def detail_card(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk)
    context = {
        'card' : card,
    }
    return render(request, 'books/detail_card.html', context)


def update_card(request, card_pk):
    card = get_object_or_404(Book, pk=card_pk)
    if request.user == card.user:
        if request.method == 'POST':
            form = CardForm(request.POST, instance=card)
            if form.is_valid():
                form.save()
                return redirect('books:detail_card', card.pk)
        else:
            form = BookForm(instance=card)
    else:
        return redirect('books:detail_card', card.pk)
    context = {
        'card' : card,
        'form' : form,
    }
    return render(request, 'books/update_card.html', context)


def delete_card(request, card_pk):
    card = get_object_or_404(Book, pk=card_pk)
    if request.user.is_authenticated:
        if request.user == card.user:
            card.delete()
            return redirect('books:index')
    return redirect('books:detail_card', card.pk)