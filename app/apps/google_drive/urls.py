from django.urls import path
from .views import create_folder_view, create_templates_view

urlpatterns = [
    path('create-folder/<str:tenant>', create_folder_view, name='create_folder'),
    path('create-templates/<str:folder_id>/<str:tenant>', create_templates_view, name='create_templates'),
]

