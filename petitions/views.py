from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Petition, Vote
from .forms import PetitionForm

def petition_list(request):
    """Display all petitions"""
    petitions = Petition.objects.all()
    context = {
        'petitions': petitions,
    }
    return render(request, 'petitions/list.html', context)

@login_required
def create_petition(request):
    """Create a new petition"""
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('petitions:list')
    else:
        form = PetitionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'petitions/create.html', context)

def petition_detail(request, petition_id):
    """Display petition details and voting interface"""
    petition = get_object_or_404(Petition, id=petition_id)
    
    # Check if user has already voted
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(petition=petition, user=request.user)
        except Vote.DoesNotExist:
            pass
    
    context = {
        'petition': petition,
        'user_vote': user_vote,
    }
    return render(request, 'petitions/detail.html', context)

@login_required
@require_POST
def vote_petition(request, petition_id):
    """Handle voting on a petition"""
    petition = get_object_or_404(Petition, id=petition_id)
    vote_type = request.POST.get('vote_type')
    
    if vote_type not in ['yes', 'no']:
        messages.error(request, 'Invalid vote type.')
        return redirect('petitions:detail', petition_id=petition_id)
    
    # Check if user has already voted
    vote, created = Vote.objects.get_or_create(
        petition=petition,
        user=request.user,
        defaults={'vote_type': vote_type}
    )
    
    if not created:
        # User already voted, update their vote
        vote.vote_type = vote_type
        vote.save()
        messages.info(request, 'Your vote has been updated.')
    else:
        messages.success(request, 'Your vote has been recorded.')
    
    return redirect('petitions:detail', petition_id=petition_id)

@login_required
@require_POST
def delete_vote(request, petition_id):
    """Remove user's vote from a petition"""
    petition = get_object_or_404(Petition, id=petition_id)
    
    try:
        vote = Vote.objects.get(petition=petition, user=request.user)
        vote.delete()
        messages.success(request, 'Your vote has been removed.')
    except Vote.DoesNotExist:
        messages.error(request, 'You have not voted on this petition.')
    
    return redirect('petitions:detail', petition_id=petition_id)