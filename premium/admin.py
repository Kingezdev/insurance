from django.contrib import admin
from .models import Premium


@admin.register(Premium)
class PremiumAdmin(admin.ModelAdmin):
    list_display = ('application', 'amount_paid', 'due_date', 'payment_date', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'due_date', 'payment_date', 'created_at')
    search_fields = ('application__client__username', 'application__policy__name', 'transaction_id', 'payment_method')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'payment_method')
    
    fieldsets = (
        ('Premium Information', {
            'fields': ('application', 'amount_paid')
        }),
        ('Payment Details', {
            'fields': ('due_date', 'payment_date', 'status', 'payment_method', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('application__client', 'application__policy')
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and obj.status == 'Paid':
            readonly.extend(['amount_paid', 'application'])
        return readonly
