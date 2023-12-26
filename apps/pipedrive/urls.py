from django.urls import path
from .views.auth import authorize_view, callback_view, oauth_success, oauth_error
from .views.webhooks import new_activity


urlpatterns = [

    path('oauth/authorize/<str:tenant>', authorize_view, name='authorize'),
    path('callback/', callback_view, name='callback'),
    path('oauth/success/', oauth_success, name="oauth_success"),
    path('oauth/error/', oauth_error, name="oauth_error"),
    path('webhook/new-activity/<str:tenant>', new_activity, name='new_activity')
]

