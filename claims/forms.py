from django import forms
from django.core.exceptions import ValidationError
from .models import Claim
from policies.models import Application


class ClaimSubmissionForm(forms.ModelForm):
    application = forms.ModelChoiceField(
        queryset=Application.objects.none(),
        empty_label="Select a policy for this claim",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Claim
        fields = ['application', 'description', 'estimated_value']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describe the incident or reason for claim in detail...',
                'class': 'form-control'
            }),
            'estimated_value': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'step': '0.01',
                'class': 'form-control',
                'min': '0'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Only show approved policies for the user
            self.fields['application'].queryset = Application.objects.filter(
                client=user,
                status='Approved'
            )
        
        self.fields['application'].label = 'Select Policy *'
        self.fields['description'].label = 'Claim Description *'
        self.fields['estimated_value'].label = 'Estimated Claim Value ($) *'
        
        # Add help text
        self.fields['description'].help_text = 'Provide detailed information about the incident, including date, time, location, and circumstances.'
        self.fields['estimated_value'].help_text = 'Enter the estimated monetary value of your claim in USD.'

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description.strip()) < 20:
            raise ValidationError('Claim description must be at least 20 characters long.')
        if len(description.strip()) > 2000:
            raise ValidationError('Claim description cannot exceed 2000 characters.')
        return description.strip()

    def clean_estimated_value(self):
        estimated_value = self.cleaned_data.get('estimated_value')
        if estimated_value <= 0:
            raise ValidationError('Estimated claim value must be greater than $0.')
        if estimated_value > 1000000:
            raise ValidationError('Estimated claim value cannot exceed $1,000,000.')
        return estimated_value

    def clean(self):
        cleaned_data = super().clean()
        application = cleaned_data.get('application')
        estimated_value = cleaned_data.get('estimated_value')
        
        if application and estimated_value:
            # Check if estimated value exceeds policy coverage
            if estimated_value > application.policy.coverage_amount:
                raise ValidationError(
                    f'Estimated value (${estimated_value:,.2f}) exceeds policy coverage '
                    f'amount (${application.policy.coverage_amount:,.2f}).'
                )
        
        return cleaned_data
