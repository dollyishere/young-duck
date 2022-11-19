from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:book_pk>/detail/', views.detail, name='detail'),
    path('<int:book_pk>/update/', views.update, name='update'),
    path('<int:book_pk>/delete/', views.delete, name='delete'),
]