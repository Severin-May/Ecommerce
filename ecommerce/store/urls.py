from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('update_profile/', views.profile_update, name='update_profile'),
    path('update_password/', views.password_update, name='update_password'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('update_profile_info/', views.profile_info_update, name='update_profile_info'),
]
