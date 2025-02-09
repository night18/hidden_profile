from django.db import models
import uuid

class CandidateProfile(models.Model):
    id = models.UUIDField(primary_key=True)
    pair = models.IntegerField()
    # Public Information
    number_of_courses_taught = models.IntegerField()
    student_teaching_evaluations = models.FloatField()
    number_of_peer_reviewed_publications = models.IntegerField()
    citation_impact = models.FloatField()
    service_on_editorial_boards = models.BooleanField()
    conference_organization_roles = models.BooleanField()
    
    # Hidden Information
    undergraduate_mentorship_success = models.BooleanField()
    graduate_thesis_supervision = models.BooleanField()
    curriculum_development = models.BooleanField()
    teaching_awards = models.BooleanField()
    
    grant_funding_secured = models.BooleanField()
    impact_of_research_publications = models.BooleanField()
    interdisciplinary_research = models.BooleanField()
    research_awards = models.BooleanField()
    
    invited_talks = models.BooleanField()
    industry_collaboration = models.BooleanField()
    university_committee_service = models.BooleanField()
    diversity_and_inclusion_initiatives = models.BooleanField()

class Participant(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker_id = models.CharField(max_length=100)
    qualification_study_id = models.CharField(max_length=100)
    qualification_seesion_id = models.CharField(max_length=100)
    formal_study_id = models.CharField(max_length=100)
    formal_session_id = models.CharField(max_length=100)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self._id)
    
class Condition(models.Model):
    """
        Condition Setting:
        -1: Not set
        0: Control (No LLM involved)
        1: Individual-level LLM
        2: Group-level LLM
    """
    _id = models.IntegerField(default=-1, primary_key=True)
    description = models.CharField(max_length=100, default="Not set")
    
    def __str__(self):
        return str(self._id)
    
    
class Role(models.Model):
    """
        Role Setting:
        0: Not set
        1: Teaching Focus
        2: Research Focus
        3: Service Focus
    """
    _id = models.IntegerField(default=0, primary_key=True)
    description = models.CharField(max_length=100, default="Not set")
    
    def __str__(self):
        return str(self._id)
    
    
class Group(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Participant, related_name='groups')
    active_participants = models.ManyToManyField(Participant, related_name='active_groups', blank=True)
    max_size = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def add_participant(self, participant):
        if self.participants.count() < self.max_size:
            self.participants.add(participant)
            self.active_participants.add(participant)
        else:
            raise ValueError("Group has reached maximum size")
    
    def remove_participant(self, participant):
        self.participants.remove(participant)
        self.active_participants.remove(participant)
        
    def inactivate_participant(self, participant):
        self.active_participants.remove(participant)
    
    def __str__(self):
        return str(self._id)

"""In case we need to run a group experiment with multiple turns"""
class Turn(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="turns")
    turn_number = models.PositiveIntegerField()
    candidate_1 = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="candidate_1")
    candidate_2 = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="candidate_2")
    candidate_3 = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="candidate_3")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    
    class Meta:
        unique_together = ('group', 'turn_number')

    def __str__(self):
        return f"Turn {self.turn_number} for Group {self.group.id}"
    
class PariticipantTurn(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('participant', 'turn')
    
    def __str__(self):
        return f"Participant {self.participant.id} in Turn {self.turn.id}"
    
    
class Message(models.Model):
    """Stores chat messages exchanged during the experiment."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Participant, on_delete=models.CASCADE)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.id} in Group {self.group.id} during Turn {self.turn.turn_number}"


class LlmMessage(models.Model):
    """Stores LLM messages exchanged during the experiment."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="llm_messages")
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="llm_messages")
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    recipient = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="llm_private_messages", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_private and self.recipient:
            return f"Private LLM Message {self.id} to {self.recipient.id} in Group {self.group.id} during Turn {self.turn.turn_number}"
        return f"Public LLM Message {self.id} in Group {self.group.id} during Turn {self.turn.turn_number}"
    
class FormalRecord(models.Model):
    """Stores each participant's vote in the formal task during the experiment."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="formal_records")
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="formal_records")
    vote = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Formal Record {self.id} from {self.participant.id} in Group {self.turn.group.id} during Turn {self.turn.turn_number}"