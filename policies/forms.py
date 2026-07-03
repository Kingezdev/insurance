from django import forms
from .models import Application


class PolicyApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Add any additional information or special requirements...',
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False
        self.fields['notes'].label = 'Additional Notes (Optional)'
