from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Policy, Application
from .forms import PolicyApplicationForm


@login_required
def browse_plans_view(request):
    """Display all available policies in Bootstrap card layout"""
    policies = Policy.objects.filter(is_active=True).order_by('name')
    
    # Get user's existing applications to show which policies they've applied for
    user_applications = Application.objects.filter(client=request.user)
    applied_policy_ids = [app.policy.id for app in user_applications]
    
    context = {
        'policies': policies,
        'applied_policy_ids': applied_policy_ids,
    }
    return render(request, 'policies/browse_plans.html', context)


@login_required
def apply_policy_view(request, policy_id):
    """Apply for a specific policy with duplicate prevention"""
    policy = get_object_or_404(Policy, id=policy_id, is_active=True)
    
    # Check if user already applied for this policy
    existing_application = Application.objects.filter(
        client=request.user, 
        policy=policy
    ).first()
    
    if existing_application:
        messages.warning(request, f'You have already applied for {policy.name} on {existing_application.applied_date.date()}. Status: {existing_application.status}')
        return redirect('policies:my_applications')
    
    if request.method == 'POST':
        form = PolicyApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = request.user
            application.policy = policy
            application.save()
            
            messages.success(request, f'Your application for {policy.name} has been submitted successfully!')
            return redirect('policies:my_applications')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PolicyApplicationForm()
    
    context = {
        'policy': policy,
        'form': form,
    }
    return render(request, 'policies/apply_policy.html', context)


@login_required
def my_applications_view(request):
    """Display user's applications with status badges"""
    applications = Application.objects.filter(client=request.user).order_by('-applied_date')
    
    context = {
        'applications': applications,
    }
    return render(request, 'policies/my_applications.html', context)


@login_required
def application_detail_view(request, application_id):
    """Show detailed view of a specific application"""
    application = get_object_or_404(Application, id=application_id, client=request.user)
    
    context = {
        'application': application,
    }
    return render(request, 'policies/application_detail.html', context)
