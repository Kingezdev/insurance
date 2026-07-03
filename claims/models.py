from django.db import models
from policies.models import Application


class Claim(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Settled', 'Settled'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='claims')
    description = models.TextField()
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    reference_no = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    settled_date = models.DateTimeField(blank=True, null=True)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    documents = models.TextField(blank=True, null=True)  # JSON field for document paths
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Claim {self.reference_no} - {self.status}"

    class Meta:
        verbose_name = "Claim"
        verbose_name_plural = "Claims"
        ordering = ['-created_at']
