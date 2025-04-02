from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count, F
from .models import CandidateProfile, Participant, Group, Role, Turn, ParticipantTurn, Message, LlmMessage, FormalRecord, Condition, InitialRecord
from .serializers import CandidateProfileSerializer
from datetime import datetime
import csv
import random

TEST_MODE = True

""" For Prolifc use"""
SUCCESS_CODE = ""
FAILED_CODE = ""
TIMEOUT_CODE = ""
IDLE_CODE = ""
""" End for Prolific use"""

@api_view(['POST'])
def create_participant(request):
    """
    In the normal mode, the request should contain the following fields:
    - worker_id: str
    - study_id: str
    - session_id: str
    In the test mode, the request should contain the following fields:
    - worker_id: str
    - study_id: None
    - session_id: None
    - condition: str
    Due to paricipant model does not have condition, hence we have to create the group but not assign the participant to the group at this momemt.
    """

    worker_id = request.POST.get('worker_id', None)
    study_id = request.POST.get('study_id', None)
    session_id = request.POST.get('session_id', None)
   
    if not worker_id:
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Check whether the participant already exists
    if Participant.objects.filter(worker_id=worker_id).exists():
        # TODO: If the participant does not complete the experiment, we should allow the participant to re-enter the experiment.
        return JsonResponse({'error': 'Participant already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Create the participant
    participant = Participant.objects.create(worker_id=worker_id, formal_study_id=study_id, formal_session_id=session_id)
    
    if TEST_MODE:
        condition_id = request.POST.get('condition', None)
        print(f"condition_id: {condition_id}")
        if not worker_id or not condition_id or condition_id not in ['0', '1', '2']:
            return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create the group
        condition = Condition.objects.get(_id=int(condition_id))
        # Check whether there is a group with the same condition and empty slot
        group = Group.objects.annotate(
            num_participants=Count('participants')
        ).filter(num_participants__lt=F('max_size'), condition=condition).order_by('created_at').first()
        
        if not group:
            group = Group.objects.create(condition=condition)
        
        
        # Assign the participant to the group
        participant.group_id = group._id
        participant.save()
        
    
    json = {
        'participant_id': participant._id,
    }
    return JsonResponse(json, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def record_avatar(request):
    participant_id = request.POST.get('participant_id', None)
    avatar_color = request.POST.get('avatar_color', None)
    avatar_animal = request.POST.get('avatar_name', None)

    if not participant_id or not avatar_color or not avatar_animal:
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    participant = Participant.objects.get(pk=participant_id)
    participant.avatar_color = avatar_color
    participant.avatar_animal = avatar_animal
    participant.save()

    return JsonResponse({'success': 'Avatar recorded'}, status=status.HTTP_200_OK)

    
@api_view(['POST'])
def pairing(request):
    participant_id = request.POST.get('participant_id', None)
    if not participant_id:
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
    participant = Participant.objects.get(pk=participant_id)
    
    """
    Check whether the participant is already assigned to a group.
    If the participant is already assigned to a group, return the group id.
    Otherwise, assign the participant to a group.
    """
    if participant.group_id:
        group_id = participant.group_id
        group = Group.objects.get(pk=group_id)
    else:
        group = Group.objects.annotate(
            num_participants=Count('participants')
        ).filter(num_participants__lt=F('max_size')).order_by('created_at').first()
    
        if not group:
            # Create a new group with random condition. Condition is a model, so we need to get the condition object first. The condition's id is from 0 to 2.
            condition = Condition.objects.order_by('?').first()
            if not condition:
                raise ValueError("No valid conditions available to create a group.") 
            group = Group.objects.create(condition=condition)
    
    
    group.add_participant(participant)
    group_id = group._id
    participant.group_id = group_id
    participant.save()
    
    json = {
        'group_id': group_id,
    }
    return JsonResponse(json, status=status.HTTP_200_OK)

@api_view(['POST'])
def initial_decision(request):
    participant_id = request.POST.get('participant_id', None)
    turn_number = request.POST.get('turn_number', None)
    selected_candidate_name = request.POST.get('selected_candidate', None)
    
    if not participant_id or not turn_number or not selected_candidate_name:
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    participant = Participant.objects.get(pk=participant_id)
    group = Group.objects.get(pk=participant.group_id)
    turn = Turn.objects.get(group=group, turn_number=turn_number)
    selected_candidate = CandidateProfile.objects.get(pair=turn_number, name=selected_candidate_name)
    
    # Store the initial decision
    InitialRecord.objects.create(participant=participant, turn=turn, vote=selected_candidate)
    
    return JsonResponse({'success': 'Initial decision recorded'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def candidate_profile_by_turn(request):
    participant_id = request.POST.get('participant_id', None)
    turn_number = request.POST.get('turn_number', None)
    
    # Get the role of the participant
    participant = Participant.objects.get(pk=participant_id)
    group = Group.objects.get(pk=participant.group_id)
    turn = Turn.objects.get(group=group, turn_number=turn_number)
    participant_turn = ParticipantTurn.objects.get(participant=participant, turn=turn)
    role_id = participant_turn.role._id
    
    # Get the candidate profiles by turn, which also named as pair in chandidate profile model
    candidate_profiles = CandidateProfile.objects.filter(pair=turn_number)
    serializer = CandidateProfileSerializer(candidate_profiles, many=True, context={'role': role_id})
    
    json = {
        "candidate_profiles": serializer.data
    }
    
    return JsonResponse(json, status=status.HTTP_200_OK)
    
    
    
    
    