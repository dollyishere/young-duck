from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('search/', views.search, name='search'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/update/', views.update_profile, name='update_profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]
