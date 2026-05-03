import uuid
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Freelancer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)
    availability = models.CharField(max_length=32, default='ad_hoc')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Ticket(models.Model):
    SERVICE_TYPES = [
        ('desktop', 'Desktop/Laptop'),
        ('linux', 'Linux Provisioning'),
        ('windows', 'Windows Provisioning'),
        ('patching', 'OS Patching'),
        ('security', 'Security Hardening'),
        ('vmware', 'VMware/Hypervisor'),
        ('sap', 'SAP Basis Lite'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPES)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(Freelancer, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_ticket_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.title} [{self.service_type}]'
