from django.contrib import admin
from django.utils import timezone
from .models import Claim


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('reference_no', 'application', 'estimated_value', 'status', 'created_at', 'approved_date', 'settled_date')
    list_filter = ('status', 'created_at', 'approved_date', 'settled_date', 'application__policy__type')
    search_fields = ('reference_no', 'application__client__username', 'application__policy__name', 'description')
    readonly_fields = ('reference_no', 'created_at', 'updated_at')
    actions = ['mark_as_under_review', 'approve_claims', 'reject_claims', 'settle_claims']
    
    fieldsets = (
        ('Claim Information', {
            'fields': ('reference_no', 'application', 'status')
        }),
        ('Claim Details', {
            'fields': ('description', 'estimated_value', 'settlement_amount')
        }),
        ('Processing Dates', {
            'fields': ('created_at', 'approved_date', 'settled_date')
        }),
        ('Additional Information', {
            'fields': ('documents', 'notes')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_under_review(self, request, queryset):
        updated = queryset.filter(status='Pending').update(status='Under Review')
        self.message_user(request, f'{updated} claim(s) marked as under review.')
    mark_as_under_review.short_description = 'Mark selected claims as under review'
    
    def approve_claims(self, request, queryset):
        updated = queryset.filter(status__in=['Pending', 'Under Review']).update(
            status='Approved', 
            approved_date=timezone.now()
        )
        self.message_user(request, f'{updated} claim(s) approved successfully.')
    approve_claims.short_description = 'Approve selected claims'
    
    def reject_claims(self, request, queryset):
        updated = queryset.filter(status__in=['Pending', 'Under Review']).update(status='Rejected')
        self.message_user(request, f'{updated} claim(s) rejected successfully.')
    reject_claims.short_description = 'Reject selected claims'
    
    def settle_claims(self, request, queryset):
        updated = queryset.filter(status='Approved').update(
            status='Settled', 
            settled_date=timezone.now()
        )
        self.message_user(request, f'{updated} claim(s) settled successfully.')
    settle_claims.short_description = 'Mark selected claims as settled'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('application__client', 'application__policy')
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and obj.status in ['Rejected', 'Settled']:
            readonly.extend(['description', 'estimated_value', 'application'])
        return readonly
