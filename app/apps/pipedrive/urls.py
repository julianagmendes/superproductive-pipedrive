from django.urls import path
from .views import new_activity


urlpatterns = [
    path('webhook/new-activity/<str:tenant>', new_activity, name='new_activity')
]

