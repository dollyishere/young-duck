from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from .models import Profile, User
from books.models import Book, Card
from movies.models import Movie
import random



# Create your views here.
# signup, login 외 모든 기능은 로그인 후 접근할 수 있으므로, 만약 해당 유저가 login 상태가 아닐 시 login 페이지로 이동하도록 조치함(is_authenticated)

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    movies = Movie.objects.all()
    backdrop_url = random.choice(movies).backdrop_path
    context = {
        'form' : form,
        'background' : f'https://image.tmdb.org/t/p/original/{backdrop_url}',
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('books:index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form = AuthenticationForm()
    movies = Movie.objects.all()
    backdrop_url = random.choice(movies).backdrop_path
    context = {
        'form' : form,
        'background' : f'https://image.tmdb.org/t/p/original/{backdrop_url}',
    }
    return render(request, 'accounts/login.html', context)


# https://ssdragon.tistory.com/92 참조
@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('accounts:login')
    return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def update(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('books:index')
        else:
            form = CustomUserChangeForm(instance=request.user)
        movies = Movie.objects.all()
        backdrop_url = random.choice(movies).backdrop_path
        context = {
            'form' : form,
            'background' : f'https://image.tmdb.org/t/p/original/{backdrop_url}',
        }
        return render(request, 'accounts/update.html', context)
    else:
        return redirect('accounts:login')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('books:index')
        else:
            form = PasswordChangeForm(request.user)
        movies = Movie.objects.all()
        backdrop_url = random.choice(movies).backdrop_path
        context = {
            'form' : form,
            'background' : f'https://image.tmdb.org/t/p/original/{backdrop_url}',
        }
        return render(request, 'accounts/change_password.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def profile(request, username):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), username=username)
        books = Book.objects.filter(user=person)
        cards = Card.objects.filter(user=person)
        context = {
            'person': person,
            'books' : books,
            'cards' : cards,
        }
        return render(request, 'accounts/profile.html', context)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def update_profile(request, username):
    if request.user.is_authenticated:
        if request.user.username == username:
            if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    return redirect('accounts:profile', username)
            else:
                form = ProfileForm(instance=request.user.profile)
            
        else:
            return redirect('accounts:profile')
        context = {
            'form' : form,
        }
        return render(request, 'accounts/update_profile.html', context)
    else:
        return redirect('accounts:login')


# follow의 경우 axios와 JsonResponse를 통해 비동기로 구현함
@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        is_followed = False
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                is_followed = False
            else:
                person.followers.add(user)
                is_followed = True
            context = {
                'is_followed' : is_followed,
                'followers_count' : person.followers.count(),
                'followings_count' : person.followings.count(),
            }
            return JsonResponse(context)
        return redirect('accounts:profile', person.username)
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searched = request.POST['searched'].strip()
            people = User.objects.filter(username__contains=searched)
            context = {
                    'searched' : searched,
                    'people' : people,
                }
            return render(request, 'accounts/search.html', context)
        else:
            return render(request, 'accounts/search.html', {})
    else:
        return redirect('accounts:login')