from django.urls import path
from .views import SignupView, authorize_view, callback_view, oauth_success, oauth_error

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    # path('oauth/authorization-platforms/<str:tenant>', authorize_view, name='authorize_view'),
    path('oauth/authorize/<str:tenant>', authorize_view, name='authorize'),
    path('callback/', callback_view, name='callback'),
    path('oauth/success/<str:tenant>', oauth_success, name="oauth_success"),
    path('oauth/error/<str:tenant>', oauth_error, name="oauth_error"),
]

