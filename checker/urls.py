from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_last_query, name='home_page'),
    path('new/', views.create_new_query, name='new_query'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('profile/',views.user_page, name='profile'),
]