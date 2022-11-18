from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

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