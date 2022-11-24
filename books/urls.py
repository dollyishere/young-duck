from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:book_pk>/detail/', views.detail, name='detail'),
    path('<int:book_pk>/update/', views.update, name='update'),
    path('<int:book_pk>/delete/', views.delete, name='delete'),
    path('<int:book_pk>/like/', views.like, name='like'),
    path('cards/create/<int:book_pk>/<int:movie_pk>/', views.create_card, name='create_card'),
    path('cards/<int:card_pk>/', views.detail_card, name='detail_card'),
    path('cards/<int:card_pk>/update/', views.update_card, name='update_card'),
    path('cards/<int:card_pk>/delete/', views.delete_card, name='delete_card'),
    path('<int:book_pk>/select/', views.select_movie, name='select_movie'),
    path('<int:book_pk>/steal/', views.steal_book, name='steal_book'),
]