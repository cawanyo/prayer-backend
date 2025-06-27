from django.urls import path
from .views import ProgramByDateView, ProgramDetailView, ProgramUpsertView,ProgramsByMonthView

urlpatterns = [
    path("program/<str:date>/", ProgramByDateView.as_view(), name="programs-by-date"),
    path('program', ProgramUpsertView.as_view(), name='program-list-create'),
    path('program/<int:pk>/', ProgramDetailView.as_view(), name='program-detail'),
    path('program/<int:year>/<int:month>/', ProgramsByMonthView.as_view(), name='programs-by-month'),
]