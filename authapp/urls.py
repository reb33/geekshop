from django.urls import path

from authapp.views import RegisterListView, LoginListView, Logout, ProfileUpdateView

app_name = 'authapp'

urlpatterns = [
    path('login', LoginListView.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', RegisterListView.as_view(), name='register'),
    path('profile', ProfileUpdateView.as_view(), name='profile'),

    path('verify/<str:email>/<str:activation_key>', RegisterListView.verify, name='verify')
]
