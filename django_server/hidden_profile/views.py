from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count, F
from .models import CandidateProfile, Participant, Group, Role, Turn, ParticipantTurn, Message, LlmMessage, FormalRecord, Condition, InitialRecord, PostSurvey, PreSurvey,   PostSurveyLLM,    PostSurveyTask,    PostSurveyNasa
from .serializers import CandidateProfileSerializer
from datetime import datetime
import csv
import random
import time
TEST_MODE = False

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
    random.seed(time.time()) 

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
            difficulty_choice = random.choice([0, 1, 2])
            
            group = Group.objects.create(
                condition=condition,
                difficulty=difficulty_choice
            )    
            
        
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
            random.seed(time.time()) 
            random_condition_id = random.choice([1])
            condition = Condition.objects.get(_id=random_condition_id)

            #condition = Condition.objects.order_by('?').first()
            #condition = Condition.objects.get(_id=0)  
            if not condition:
                raise ValueError("No valid conditions available to create a group.") 
            difficulty_choice = random.choice([ 2])
            
            group = Group.objects.create(
                condition=condition,
                difficulty=difficulty_choice
            )    
    
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
    print(selected_candidate_name)
    selected_candidate = CandidateProfile.objects.get(name=selected_candidate_name, difficult=group.difficulty)
    
    # Store the initial decision
    InitialRecord.objects.create(participant=participant, turn=turn, vote=selected_candidate)
    
    return JsonResponse({'success': 'Initial decision recorded'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def final_decision(request):
    participant_id = request.POST.get('participant_id', None)
    turn_number = request.POST.get('turn_number', None)
    selected_candidate_id = request.POST.get('selected_candidate', None)
    
    if not participant_id or not turn_number or not selected_candidate_id:
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    participant = Participant.objects.get(pk=participant_id)
    group = Group.objects.get(pk=participant.group_id)
    turn = Turn.objects.get(group=group, turn_number=turn_number)
    selected_candidate = CandidateProfile.objects.get(pk=selected_candidate_id, difficult=group.difficulty)
    
    # Store the final decision
    FormalRecord.objects.create(participant=participant, turn=turn, vote=selected_candidate)
    
    return JsonResponse({'success': 'Final decision recorded'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def candidate_profile_by_turn(request):
    participant_id = request.POST.get('participant_id', None)
    turn_number = request.POST.get('turn_number', None)
    
    # Get the role of the participant
    participant = Participant.objects.get(pk=participant_id)
    group = Group.objects.get(pk=participant.group_id)
    turn = Turn.objects.get(group=group, turn_number=turn_number)
    # update turn with turn_number
    turn.candidatePair = turn_number
    turn.save()
    
    participant_turn = ParticipantTurn.objects.get(participant=participant, turn=turn)
    role_id = participant_turn.role._id
    
    # Get the candidate profiles by turn, which also named as pair in chandidate profile model
    candidate_profiles = CandidateProfile.objects.filter(pair=turn_number, difficult=group.difficulty)
    serializer = CandidateProfileSerializer(candidate_profiles, many=True, context={'role': role_id})
    
    json = {
        "candidate_profiles": serializer.data
    }
    
    return JsonResponse(json, status=status.HTTP_200_OK)
@api_view(['POST'])
def record_pre_survey(request):
    """
    Records the participant's responses to the pre-survey.
    """
    participant_id = request.data.get('participant_id', None)
    if not participant_id:
        return JsonResponse({'error': 'Missing participant_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        participant = Participant.objects.get(pk=participant_id)
    except Participant.DoesNotExist:
        return JsonResponse({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if participant already has a pre-survey record
    if PreSurvey.objects.filter(participant=participant).exists():
        return JsonResponse({'error': 'Pre-survey already completed for this participant'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Extract survey responses from the request
        # Note: The frontend sends 'ml_knowledge', but the model field is 'ai_knowledge'.
        survey_data = {
            'ai_knowledge': request.data.get('ai_knowledge'),
            'gender': request.data.get('gender'),
            'age': request.data.get('age'),
            'ethnicity': request.data.get('ethnicity'),
            'education': request.data.get('education'),
        }

        # Validate that all required fields are present
        if any(value is None or value == '' for value in survey_data.values()):
            return JsonResponse({'error': 'Missing required survey fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the PreSurvey record
        pre_survey = PreSurvey.objects.create(
            participant=participant,
            **survey_data
        )

        return JsonResponse({'message': 'Pre-survey recorded successfully', 'survey_id': str(pre_survey._id)}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred while saving the survey: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def record_post_survey_llm(request):
    """Records the LLM part of the post-survey."""
    participant_id = request.data.get('participant_id')
    try:
        participant = Participant.objects.get(pk=participant_id)
        survey_data = {
            'open_ended_response': request.data.get('open_ended_response'),
            'llm_summary': request.data.get('llm_summary'),
            'llm_encouragement': request.data.get('llm_encouragement'),
            'llm_alternatives': request.data.get('llm_alternatives'),
            'llm_collaboration': request.data.get('llm_collaboration'),
            'llm_satisfaction': request.data.get('llm_satisfaction'),
            'llm_quality': request.data.get('llm_quality'),
            'llm_recommendation': request.data.get('llm_recommendation'),
            'llm_future_use': request.data.get('llm_future_use'),
        }
        PostSurveyLLM.objects.create(participant=participant, **survey_data)
        return JsonResponse({'message': 'LLM survey recorded successfully'}, status=200)
    except Participant.DoesNotExist:
        return JsonResponse({'error': 'Participant not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['POST'])
def record_post_survey_task(request):
    """Records the task-related part of the post-survey."""
    participant_id = request.data.get('participant_id')
    try:
        participant = Participant.objects.get(pk=participant_id)
        survey_data = {
            'dialogue_management': request.data.get('dialogue_management'),
            'information_pooling': request.data.get('information_pooling'),
            'reaching_consensus': request.data.get('reaching_consensus'),
            'time_management': request.data.get('time_management'),
            'reciprocal_interaction': request.data.get('reciprocal_interaction'),
            'individual_task_orientation': request.data.get('individual_task_orientation'),
        }
        PostSurveyTask.objects.create(participant=participant, **survey_data)
        return JsonResponse({'message': 'Task survey recorded successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['POST'])
def record_post_survey_nasa(request):
    """Records the NASA-TLX part of the post-survey."""
    participant_id = request.data.get('participant_id')
    try:
        participant = Participant.objects.get(pk=participant_id)
        survey_data = {
            'mental_demand': request.data.get('mental_demand'),
            'temporal_demand': request.data.get('temporal_demand'),
            'performance': request.data.get('performance'),
            'effort': request.data.get('effort'),
            'frustration': request.data.get('frustration'),
        }
        PostSurveyNasa.objects.create(participant=participant, **survey_data)
        return JsonResponse({'message': 'NASA-TLX survey recorded successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
@api_view(['POST'])
def get_bonus(request):
    participant_id = request.POST.get('participant_id', None)
    if not participant_id:
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    participant = Participant.objects.get(pk=participant_id)
    group = Group.objects.get(pk=participant.group_id)
    turns = Turn.objects.filter(group=group)
    
    total_bonus = 0
    voting_results = []  # List to store voting results for each turn
    
    for turn in turns:
        # Get all formal records for the turn
        votes = FormalRecord.objects.filter(turn=turn).values_list('vote', flat=True)
        if not votes:
            continue
        
        # Determine the majority vote
        vote_counts = {}
        for vote in votes:
            vote_counts[vote] = vote_counts.get(vote, 0) + 1
        
        majority_vote = max(vote_counts, key=vote_counts.get)
        if list(vote_counts.values()).count(vote_counts[majority_vote]) > 1:
            # Tie in votes, no bonus for this turn
            voting_results.append({
                'task': f'Turn {turn.turn_number}',
                'final_vote': 'Tie',
                'ground_truth': 'N/A',
                'bonus': 0
            })
            continue
        
        # Check if the majority vote corresponds to the best candidate
        best_candidate = CandidateProfile.objects.filter(difficult=group.difficulty,     winner=True).first()
        bonus = 1.5 if best_candidate and str(best_candidate._id) == str(majority_vote) else 0
        total_bonus += bonus

        final_vote_name = CandidateProfile.objects.get(pk=majority_vote).name if majority_vote else 'N/A'
        
        voting_results.append({
            'task': str(turn.turn_number),
            'final_vote': str(final_vote_name),
            'ground_truth': str(best_candidate) if best_candidate else 'N/A',
            'bonus': bonus
        })
    
    # Save the bonus to the participant
    participant.bonus = total_bonus
    participant.end_time = datetime.now()
    participant.save()
    
    return JsonResponse({'bonus': total_bonus, 'list': voting_results}, status=status.HTTP_200_OK)
