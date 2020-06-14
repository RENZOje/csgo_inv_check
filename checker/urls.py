from django.urls import path
from django.views.generic import DetailView
from .models import *

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.get_last_query, name='home_page'),
    path('new/', views.create_new_query, name='new_query'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.user_page, name='profile'),
    path('help/', views.help, name='help'),

    path('query/refresh/', views.refresh_query, name='query_refresh'),
    path('query/<int:pk>/', views.get_detail_query, name='query_detail'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
         name='password_reset_complete'),

]
