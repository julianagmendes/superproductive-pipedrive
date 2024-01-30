from django.urls import path
from .views import SignupView, authorize_view_calendly, authorize_view_pipedrive, \
                        callback_view, AuthenticatePlatformsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('authenticate-platforms/<str:tenant>', AuthenticatePlatformsView.as_view(), name='authenticate_platforms'),
    path('oauth/authorize-pipedrive/<str:tenant>', authorize_view_pipedrive, name='authorize_pipedrive'),
    path('oauth/authorize-calendly/<str:tenant>', authorize_view_calendly, name='authorize_calendly'),
    path('callback/', callback_view, name='callback')
]

