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
# 데코레이터 공식은 https://ssdragon.tistory.com/92 참조


@require_http_methods(['GET', 'POST'])
def signup(request):
    # 만약 로그인 한 유저일 시, 메인 페이지(books/index.html)로 이동합니다.
    if request.user.is_authenticated:
        return redirect('books:index')

    # 만약 접근 방식이 POST라면 사용자가 입력한 데이터를 request.POST를 통해 불러와 form에 넣어줍니다.
    # 만약 회원 가입 form이 valid하다면, 신규 유저를 생성하고 로그인합니다.
    # profile의 경우, 신규 유저 생성 시 동시에 생성됩니다.
    # 이때 초기 nickname, profile_img도 임의로 지정해줍니다.
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile_form = ProfileForm()
            my_profile = profile_form.save(commit=False)
            my_profile.user = user
            my_profile.nickname = '{}번째 수집가'.format(user.pk)
            my_profile.profile_img = 'images/icons/{}.png'.format(random.randrange(1, 20))
            my_profile.save()
            auth_login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    
    # 만약 GET으로 접근했을 시에는, 유저 생성 화면으로 이동합니다.
    # 이때 배경화면에는 movies의 백드롭 이미지를 랜덤으로 받아와 저장한 후, html에서 입혀줍니다.
    movies = Movie.objects.all()
    backdrop_url = random.choice(movies).backdrop_path
    context = {
        'form' : form,
        'background' : f'https://image.tmdb.org/t/p/original/{backdrop_url}',
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    # 만약 이미 로그인한 사용자라면, 메인 화면으로 이동합니다.
    if request.user.is_authenticated:
        return redirect('books:index')
    
    # 만약 접근 방식이 POST라면, 로그인 form에 request.POST에 담긴 정보를 넣어줍니다.
    # 이후 form의 형식이 valid하다면, 로그인을 진행합니다.
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    
    # 만약 GET으로 접근했다면, 로그인 화면으로 이동합니다.
    # signup과 마찬가지로 movies에 저장된 백드롭 이미지를 랜덤으로 받아와 저장한 후, html에서 입혀줍니다.
    else:
        form = AuthenticationForm()
    movies = Movie.objects.all()
    backdrop_url = random.choice(movies).backdrop_path
    context = {
        'form' : form,
        'background' : f'https://image.tmdb.org/t/p/original/{backdrop_url}',
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    # 만약 사용자가 로그인했다면, 로그아웃합니다.
    # 이후 로그인 화면으로 이동합니다.
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def update(request):
    if request.user.is_authenticated:
        # 만약 접근 방식이 POST이고, form이 valid하다면 유저 정보 업데이트를 진행합니다.
        # 업데이트 후에는 메인 화면으로 이동합니다.
        # GET으로 접근했다면, 유저 정보 업데이트 화면으로 이동합니다.
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
    # 만약 유저가 로그인한 상태라면, 유저 정보를 삭제한 후, 로그아웃을 진행합니다.
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.user.is_authenticated:
        # 만약 POST로 접근하고, 이후 불러온 정보로 구성된 form이 valid하다면, 비밀번호 수정을 진행합니다.
        # 업데이트 이후에는 메인 화면으로 이동합니다.
        # 만약 GET으로 접근했을 시에는 유저 비밀번호 수정 화면으로 이동합니다.
        # 이때 배경화면에는 movies의 백드롭 이미지를 랜덤으로 받아와 저장한 후, html에서 입혀줍니다.
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
        # username과 대조하여 해당 유저에 대한 정보를 불러옵니다.
        # 이후 해당 유저가 작성한 테마북과 카드에 대한 정보를 filter를 통해 불러옵니다.
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
        # 만약 요청한 유저와 해당 프로필의 소유자인 유저의 username이 일치하다면, 프로필 수정을 가능하게 합니다.
        # 만약 POST로 접근했고, 해당 정보를 담은 form이 valid하다면 프로필 수정을 진행합니다.
        # 만약 GET으로 접근했다면 프로필 수정 화면으로 이동합니다.
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


# follow의 경우 axios와 JsonResponse를 통해 비동기로 구현했습니다.
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
        # 만약 POST로 접근했다면, request.POST를 통해 사용자가 검색창에 입력한 값을 불러와 stirp()로 공백을 제거합니다.
        # 이후 해당 검색어를 username, nickname에 포함하고 있는 유저를 filter와 __contains를 통해 정보를 불러와 people에 저장합니다.
        if request.method == 'POST':
            searched = request.POST['searched'].strip()
            people = []
            
            people_username = User.objects.filter(username__contains=searched)
            if people_username:
                people.extend(people_username)
            
            profile_nickname = Profile.objects.filter(nickname__contains=searched)
            
            for person_nickname in profile_nickname:
                if person_nickname.user not in people:
                    people.append(person_nickname.user)

            context = {
                    'searched' : searched,
                    'people' : people,
                }
            return render(request, 'accounts/search.html', context)
        else:
            return render(request, 'accounts/search.html', {})
    else:
        return redirect('accounts:login')