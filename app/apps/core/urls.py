from django.urls import path
from .views import SignupView, authorize_view_google_drive, authorize_view_pipedrive, \
                        callback_view, AuthenticatePlatformsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('authenticate-platforms/<str:tenant>', AuthenticatePlatformsView.as_view(), name='authenticate_platforms'),
    path('oauth/authorize-pipedrive/<str:tenant>', authorize_view_pipedrive, name='authorize_pipedrive'),
    path('oauth/authorize-google-drive/<str:tenant>', authorize_view_google_drive, name='authorize_google_drive'),
    path('callback/', callback_view, name='callback'),
    # path('<str:tenant>', index, name='index'),
    # path('get-data/<str:button_name>/<str:tenant>/', get_data, name='get_data'),
    # path('update-data/<str:button_name>/<str:tenant>/', update_data, name='update_data'),

]

