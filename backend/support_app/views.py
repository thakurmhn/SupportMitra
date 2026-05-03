from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer, Ticket
from .serializers import CustomerSerializer, TicketSerializer, UserSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    return Response({'status': 'ok', 'timestamp': timezone.now()})


class ServiceListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        services = [
            {'key': 'desktop', 'name': 'Desktop / Laptop Support'},
            {'key': 'linux', 'name': 'Linux Provisioning'},
            {'key': 'windows', 'name': 'Windows Provisioning'},
            {'key': 'patching', 'name': 'OS Patching'},
            {'key': 'security', 'name': 'Security Hardening'},
            {'key': 'vmware', 'name': 'VMware / Hypervisor Support'},
            {'key': 'sap', 'name': 'SAP Basis Lite'},
        ]
        return Response(services)


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        if not username or not password:
            return Response({'detail': 'username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=request.data.get('email'), password=password)
        Customer.objects.create(user=user, company=request.data.get('company', ''), phone=request.data.get('phone', ''))
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Ticket.objects.filter(customer=customer).order_by('-created_at')

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        serializer.save(customer=customer)


class TicketDetailView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.customer.user != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)
