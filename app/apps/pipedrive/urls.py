from django.urls import path
from .views import get_all_webhooks_view, delete_webhook_view, added_deal, updated_deal



urlpatterns = [
    path('get-all-webhooks/<str:tenant>', get_all_webhooks_view, name='get_all_webhooks'),
    path('delete-webhook/<int:webhook_id>/<str:tenant>', delete_webhook_view, name='delete_webhook'),
    path('webhook/added-deal/<str:tenant>', added_deal, name='added_deal'),
    path('webhook/updated-deal/<str:tenant>', updated_deal, name='updated_deal'),

]

