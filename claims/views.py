from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Claim
from .forms import ClaimSubmissionForm
from policies.models import Application


@login_required
def submit_claim_view(request):
    """Submit a claim tied to an approved policy"""
    # Get user's approved policies (applications with Approved status)
    approved_applications = Application.objects.filter(
        client=request.user,
        status='Approved'
    )
    
    if not approved_applications.exists():
        messages.warning(request, 'You need at least one approved policy to submit a claim.')
        return redirect('policies:my_applications')
    
    if request.method == 'POST':
        form = ClaimSubmissionForm(request.POST, user=request.user)
        if form.is_valid():
            claim = form.save(commit=False)
            # Generate unique reference number
            import uuid
            claim.reference_no = f"CLM-{uuid.uuid4().hex[:8].upper()}"
            claim.save()
            
            messages.success(request, f'Your claim has been submitted successfully! Reference number: {claim.reference_no}')
            return redirect('claims:claim_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClaimSubmissionForm(user=request.user)
    
    context = {
        'form': form,
        'approved_applications': approved_applications,
    }
    return render(request, 'claims/submit_claim.html', context)


@login_required
def claim_list_view(request):
    """Display user's claims with status and reference numbers"""
    claims = Claim.objects.filter(
        application__client=request.user
    ).order_by('-created_at')
    
    context = {
        'claims': claims,
    }
    return render(request, 'claims/claim_list.html', context)


@login_required
def claim_detail_view(request, claim_id):
    """Show detailed view of a specific claim"""
    claim = get_object_or_404(
        Claim, 
        id=claim_id, 
        application__client=request.user
    )
    
    context = {
        'claim': claim,
    }
    return render(request, 'claims/claim_detail.html', context)
