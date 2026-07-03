from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import UserProfile
import re


class CustomRegistrationForm(UserCreationForm):
    surname = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your surname'
        })
    )
    firstname = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    phone = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    role = forms.ChoiceField(
        choices=[
            ('client', 'Client'),
            ('admin', 'Administrator'),
        ],
        initial='client',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'surname', 'firstname', 'email', 'phone', 'date_of_birth', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
        
        # Add help text
        self.fields['surname'].help_text = 'Your family name or last name'
        self.fields['firstname'].help_text = 'Your given name or first name'
        self.fields['phone'].help_text = 'Include country code if outside US'
        self.fields['date_of_birth'].help_text = 'You must be at least 18 years old'
        self.fields['role'].help_text = 'Select your role in the system'

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not surname.replace(' ', '').isalpha():
            raise ValidationError('Surname should only contain letters and spaces.')
        return surname.title()

    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        if not firstname.replace(' ', '').isalpha():
            raise ValidationError('First name should only contain letters and spaces.')
        return firstname.title()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Remove all non-digit characters for validation
        phone_digits = re.sub(r'[^\d]', '', phone)
        if len(phone_digits) < 10:
            raise ValidationError('Phone number must contain at least 10 digits.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email.lower()

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = timezone.now().date()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        
        if age < 18:
            raise ValidationError('You must be at least 18 years old to register.')
        if age > 120:
            raise ValidationError('Please enter a valid date of birth.')
        return date_of_birth

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Create UserProfile with additional fields
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user
