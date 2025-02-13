from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from rides import views
from .views import create_ride

urlpatterns = [
    path('', views.ride_list, name='ride_list'),
    path('create/', create_ride, name='create_ride'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('rides/<int:ride_id>/book/', views.create_booking, name='create_booking'),
    path('bookings/', views.booking_requests, name='booking_requests'),
    path('bookings/<int:booking_id>/<str:action>/', views.manage_booking, name='manage_booking'),
]