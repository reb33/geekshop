from django.urls import path

from authapp.views import login, register, logout, profile

app_name = 'authapp'

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),
    path('profile', profile, name='profile')
]
