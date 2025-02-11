from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count, F
from .models import CandidateProfile, Participant, Group, Role, Turn, PariticipantTurn, Message, LlmMessage, FormalRecord, Condition
# from .serializers import CandidateProfileSerializer, ParticipantSerializer, GroupSerializer, RoleSerializer, TurnSerializer, PariticipantTurnSerializer, MessageSerializer, LlmMessageSerializer, FormalRecordSerializer
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
    

    