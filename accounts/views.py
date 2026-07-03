from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import CustomRegistrationForm
from policies.models import Application
from premium.models import Premium
from claims.models import Claim


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Assign admin role if selected
            role = form.cleaned_data.get('role')
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            
            user.save()
            
            # Update user profile (created by signal)
            from .models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.surname = form.cleaned_data['surname']
            profile.firstname = form.cleaned_data['firstname']
            profile.phone = form.cleaned_data['phone']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            profile.save()
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    user = request.user
    
    # Get user's applications, premiums, and claims
    applications = Application.objects.filter(client=user).order_by('-applied_date')
    premiums = Premium.objects.filter(application__client=user).order_by('-due_date')
    claims = Claim.objects.filter(application__client=user).order_by('-created_at')
    
    # Get active policies (approved applications)
    active_policies = applications.filter(status='Approved')
    
    # Calculate statistics
    total_applications = applications.count()
    active_policies_count = active_policies.count()
    pending_applications = applications.filter(status='Pending').count()
    rejected_applications = applications.filter(status='Rejected').count()
    
    # Premium calculations
    total_premiums_paid = premiums.filter(status='Paid').count()
    pending_premiums = premiums.filter(status='Pending').count()
    overdue_premiums = premiums.filter(status='Overdue').count()
    
    # Get next due premium
    next_due_premium = premiums.filter(status='Pending').order_by('due_date').first()
    
    # Claims calculations
    total_claims = claims.count()
    pending_claims = claims.filter(status='Pending').count()
    approved_claims = claims.filter(status='Approved').count()
    
    context = {
        'user': user,
        'applications': applications[:5],  # Recent 5 applications
        'premiums': premiums[:5],  # Recent 5 premiums
        'claims': claims[:5],  # Recent 5 claims
        'active_policies': active_policies[:5],  # Recent 5 active policies
        'next_due_premium': next_due_premium,
        'stats': {
            'total_applications': total_applications,
            'active_policies': active_policies_count,
            'pending_applications': pending_applications,
            'rejected_applications': rejected_applications,
            'total_premiums_paid': total_premiums_paid,
            'pending_premiums': pending_premiums,
            'overdue_premiums': overdue_premiums,
            'total_claims': total_claims,
            'pending_claims': pending_claims,
            'approved_claims': approved_claims,
        }
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def admin_applications_view(request):
    """View for admins to manage applications"""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard')
    
    # Get applications by status
    from policies.models import Application
    pending_applications = Application.objects.filter(status='Pending')
    approved_applications = Application.objects.filter(status='Approved')
    rejected_applications = Application.objects.filter(status='Rejected')
    
    context = {
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
    }
    
    return render(request, 'accounts/admin_applications.html', context)


@login_required
def approve_application_view(request, application_id):
    """Approve an application and automatically generate premiums"""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to approve applications.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        from policies.models import Application
        try:
            application = Application.objects.get(id=application_id)
            
            if application.status != 'Pending':
                messages.warning(request, 'This application has already been processed.')
                return redirect('accounts:admin_applications')
            
            # Update application status
            application.status = 'Approved'
            application.approved_date = timezone.now()
            application.save()
            
            messages.success(request, f'Application #{application.id} has been approved. Premiums have been automatically generated.')
            
        except Application.DoesNotExist:
            messages.error(request, 'Application not found.')
    
    return redirect('accounts:admin_applications')


@login_required
def reject_application_view(request, application_id):
    """Reject an application"""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to reject applications.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        from policies.models import Application
        try:
            application = Application.objects.get(id=application_id)
            
            if application.status != 'Pending':
                messages.warning(request, 'This application has already been processed.')
                return redirect('accounts:admin_applications')
            
            # Update application status
            application.status = 'Rejected'
            application.rejected_date = timezone.now()
            application.save()
            
            messages.success(request, f'Application #{application_id} has been rejected.')
            
        except Application.DoesNotExist:
            messages.error(request, 'Application not found.')
    
    return redirect('accounts:admin_applications')
