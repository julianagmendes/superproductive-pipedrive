from django.urls import path
from .views import signup_view

urlpatterns = [
    path('signup/<str:tenant>', signup_view, name='signup'),
]

