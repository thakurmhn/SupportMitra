from django.contrib import admin
from .models import Customer, Freelancer, Ticket


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'phone', 'created_at')


@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ('user', 'availability', 'active', 'created_at')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'service_type', 'status', 'assigned_to', 'created_at')
    list_filter = ('service_type', 'status')
