from django.contrib import admin
from django.utils import timezone
from .models import Policy, Application
from premium.models import Premium


class PremiumInline(admin.TabularInline):
    model = Premium
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('amount_paid', 'payment_date', 'due_date', 'status', 'payment_method', 'transaction_id', 'created_at', 'updated_at')


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'premium_amount', 'coverage_amount', 'duration_months', 'is_active', 'created_at')
    list_filter = ('type', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'type')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Policy Information', {
            'fields': ('name', 'type', 'description')
        }),
        ('Financial Details', {
            'fields': ('premium_amount', 'coverage_amount', 'duration_months')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('client', 'policy', 'status', 'applied_date', 'approved_date', 'rejected_date')
    list_filter = ('status', 'policy__type', 'applied_date', 'approved_date')
    search_fields = ('client__username', 'client__email', 'policy__name', 'notes')
    readonly_fields = ('applied_date', 'updated_at')
    inlines = [PremiumInline]
    actions = ['approve_applications', 'reject_applications']
    
    fieldsets = (
        ('Application Details', {
            'fields': ('client', 'policy', 'status')
        }),
        ('Dates', {
            'fields': ('applied_date', 'approved_date', 'rejected_date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def approve_applications(self, request, queryset):
        updated = queryset.filter(status='Pending').update(
            status='Approved', 
            approved_date=timezone.now()
        )
        self.message_user(request, f'{updated} application(s) approved successfully.')
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        updated = queryset.filter(status='Pending').update(
            status='Rejected', 
            rejected_date=timezone.now()
        )
        self.message_user(request, f'{updated} application(s) rejected successfully.')
    reject_applications.short_description = 'Reject selected applications'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('client', 'policy')
