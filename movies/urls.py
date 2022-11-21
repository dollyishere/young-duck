from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('recommended/', views.recommended, name='recommended'),
    path('search/', views.search, name='search'),
    path('<int:movie_pk>/search/', views.search_book, name='search_book'),
]
