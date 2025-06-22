from django.contrib import admin
from django.urls import path

from .views import (
    PrayerListView,
    PrayerCreateView,
    PrayerDetailView,
    PrayerCategoryListCreateView,
    PrayerCategoryDetailView,
    user_prayers,
    update_prayer_state,
    PrayerCommentListCreateView
)

urlpatterns = [
    path("", PrayerCreateView.as_view(), name='prayer-create'),
    path("list/", PrayerListView.as_view(), name='prayer-create'),
    path('<int:pk>/', PrayerDetailView.as_view(), name='prayer-detail'),
    path('me/', user_prayers, name='user-prayers'),
    path('categories/', PrayerCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', PrayerCategoryDetailView.as_view(), name='category-detail'),
    path('<int:prayer_id>/comments/', PrayerCommentListCreateView.as_view(), name='prayer-comments'),
    path('<int:pk>/update-state/', update_prayer_state, name='update-prayer-state'),
]
