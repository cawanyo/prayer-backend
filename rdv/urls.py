from django.urls import path
from .views import RDVCreateView, RDVListView, ValidateRDVAvailabilityView, RDVByDateView, RDVUpdateView, AvailabilityView, DeleteRDVView, AllRDVListView

urlpatterns = [
    path('', RDVListView.as_view(), name='list-rdvs'),
    path('all/', AllRDVListView.as_view(), name='list-rdvs-all'),
    path('delete/<int:pk>/', DeleteRDVView.as_view(), name='delete-rdv'),
    path('create/', RDVCreateView.as_view(), name='create-rdv'),
    path('date/<str:date>/', RDVByDateView.as_view(), name='rdv-by-date'),
    path('<int:rdv_id>/validate/<int:avail_id>/', ValidateRDVAvailabilityView.as_view(), name='validate-rdv'),
    path('<int:pk>/update/', RDVUpdateView.as_view(), name='rdv-update'),
    
    path('availability/<int:pk>/', AvailabilityView.as_view())
]