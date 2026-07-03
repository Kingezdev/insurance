from django.db import models
from django.contrib.auth.models import User


class Policy(models.Model):
    POLICY_TYPES = [
        ('Life', 'Life Insurance'),
        ('Motor', 'Motor Insurance'),
        ('Health', 'Health Insurance'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=POLICY_TYPES)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
        ordering = ['-created_at']


class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    rejected_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client.username} - {self.policy.name} - {self.status}"

    class Meta:
        verbose_name = "Policy Application"
        verbose_name_plural = "Policy Applications"
        ordering = ['-applied_date']
