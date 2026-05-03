from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer, Ticket, Freelancer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'company', 'phone', 'created_at', 'updated_at']


class FreelancerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Freelancer
        fields = ['id', 'user', 'skills', 'availability', 'active', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'customer', 'title', 'service_type', 'status', 'assigned_to', 'created_at', 'updated_at', 'external_ticket_id']
        read_only_fields = ['status', 'created_at', 'updated_at']
