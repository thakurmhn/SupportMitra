from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('health/', views.health_check, name='health'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tickets/', views.TicketListCreateView.as_view(), name='ticket_list_create'),
    path('tickets/<uuid:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
]
