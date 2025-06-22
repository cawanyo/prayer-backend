from django.urls import path
from .views import AvailabilityUpsertView, AvailabilityView, AvailableUsersByDate

urlpatterns = [
    path('<str:date>/upsert/', AvailabilityUpsertView.as_view(), name='availability-upsert'),
    path('<str:date>/', AvailabilityView.as_view(), name='availability'),
    path('users/<str:date>/', AvailableUsersByDate.as_view(), name='available-users-by-date'),

]