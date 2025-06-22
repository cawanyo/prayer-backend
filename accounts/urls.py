from django.urls import path
from .views import (
    RegisterUserView, 
    check_username, 
    check_email, 
    MemberDemandCreateView, 
    MemberDemandListView, 
    MemberDemandUpdateView, 
    current_user_view,
    is_intercesseur,
    is_responsable,
    MembershipRequestView,
    UpdateOwnInfoView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('check-username/', check_username, name='check-username' ),
    path('check-email/', check_email, name='check-email' ),
    
    path('me/', current_user_view, name='current-user'),
    path('me/update/', UpdateOwnInfoView.as_view(), name='user-update-info'),
    
    path('demands/', MemberDemandCreateView.as_view(), name='member-demand-create'),
    path('demands/status/', MembershipRequestView.as_view(), name='membership-request-status'),
    path('list-demands/', MemberDemandListView.as_view(), name='member-demand-list-view'),
    path('demands/<int:pk>/', MemberDemandUpdateView.as_view(), name='member-demand-update'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('is-intercesseur/', is_intercesseur, name='is-intercesseur'),
    path('is-responsable/', is_responsable, name='is-intercesseur'),
    
]