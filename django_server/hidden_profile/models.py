from django.db import models
import uuid

class CandidateProfile(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pair = models.IntegerField()
    difficult = models.IntegerField(default=0)  # 0: easy, 1: difficult
    winner = models.BooleanField()
    # Public Information
    name = models.CharField(max_length=100)
    #number_of_courses_taught = models.CharField(max_length=100)
    #student_teaching_evaluations =models.CharField(max_length=100)
    publications = models.CharField(max_length=100)
    citations = models.CharField(max_length=100)
    editorial_service = models.CharField(max_length=100)
    conference_organization = models.CharField(max_length=100)
    
    # Hidden Information
    mentorship = models.CharField(max_length=100)
    #graduate_thesis_supervision = models.CharField(max_length=100)
    #curriculum_development = models.CharField(max_length=100)
    teaching = models.CharField(max_length=100)
    
    funding = models.CharField(max_length=100)
    #reviewer_activity = models.CharField(max_length=100)
    interdisciplinarity = models.CharField(max_length=100)
    #research_awards = models.CharField(max_length=100)
    
    #invited_talks = models.CharField(max_length=100)
    collaborations = models.CharField(max_length=100)
    #university_committee_service = models.CharField(max_length=100)
    research_coverage = models.CharField(max_length=100)
    def __str__(self):
        return str(self.name)

class Participant(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker_id = models.CharField(max_length=100)
    qualification_study_id = models.CharField(max_length=100)
    qualification_seesion_id = models.CharField(max_length=100)
    formal_study_id = models.CharField(max_length=100)
    formal_session_id = models.CharField(max_length=100)
    avatar_color = models.CharField(max_length=100, default=None, null=True)
    avatar_animal = models.CharField(max_length=100, default=None, null=True)
    group_id = models.UUIDField( null=True, blank=True)
    bonus = models.FloatField(default=0.0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    complete_initial = models.BooleanField(default=False)   
    auto_llm = models.BooleanField(default=False)   

    class Meta:
        ordering = ['-start_time'] #
    
    def __str__(self):
        return str(self._id)
    
class Condition(models.Model):
    """
        Condition Setting:
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
    difficulty = models.IntegerField(default=0)  # 0: easy, 1: difficult
    class Meta:
        ordering = ['-created_at'] 

    def is_full(self):
        return self.participants.count() >= self.max_size
    
    def add_participant(self, participant):
        if self.participants.count() < self.max_size:
            self.participants.add(participant)
        else:
            raise ValueError("Group has reached maximum size")
    
    def remove_participant(self, participant):
        self.participants.remove(participant)
        self.active_participants.remove(participant)
        
    def activate_participant(self, participant):
        self.active_participants.add(participant)    
    
    def inactivate_participant(self, participant):
        self.active_participants.remove(participant)
    
    def __str__(self):
        return str(self._id)

"""In case we need to run a group experiment with multiple turns"""
class Turn(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="turns")
    turn_number = models.PositiveIntegerField()
    candidatePair = models.IntegerField(null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    
    class Meta:
        unique_together = ('group', 'turn_number')

    def __str__(self):
        return f"Turn {self.turn_number} for Group {self.group._id}"
    
class ParticipantTurn(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('participant', 'turn')
    
    def __str__(self):
        return str(self._id)
    
    
class Message(models.Model):
    """Stores chat messages exchanged during the experiment."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Participant, on_delete=models.CASCADE)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    quori_included = models.BooleanField(default=False)
    class Meta:
        ordering = ['-timestamp'] # Example: Ensure logic matches fields that exist!


    def __str__(self):
        return f"Message {self._id} from {self.sender._id} in Group {self.group._id} during Turn {self.turn.turn_number}"


class LlmMessage(models.Model):
    """Stores LLM messages exchanged during the experiment."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="llm_messages")
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="llm_messages")
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    is_summary = models.BooleanField(default=False)
    recipient = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="llm_private_messages", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_intervention_analysis=models.BooleanField(default=False)
    type_of_intervention = models.CharField(max_length=100, null=True, blank=True)
    input_messages = models.TextField(default="")
    class Meta:
        ordering = ['-timestamp'] 

    def __str__(self):
        if self.is_private and self.recipient:
            return f"Private LLM Message {self._id} to {self.recipient._id} in Group {self.group._id} during Turn {self.turn.turn_number}"
        return f"Public LLM Message {self._id} in Group {self.group._id} during Turn {self.turn.turn_number}"

class InitialRecord(models.Model):
    """Stores each participant's vote in the initial task during the experiment."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="initial_records")
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="initial_records")
    vote = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="initial_records")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Initial Record {self._id} from {self.participant._id} in Group {self.turn.group._id} during Turn {self.turn.turn_number}"

class FormalRecord(models.Model):
    """Stores each participant's vote in the formal task during the experiment."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="formal_records")
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="formal_records")
    vote = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="formal_records")
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp'] 

    def __str__(self):
        return f"Formal Record {self._id} from {self.participant._id}, voting {self.vote.name}, in Group {self.turn.group._id} during Turn {self.turn.turn_number}"
    
class PostSurvey(models.Model):
    """Stores each participant's post-survey responses."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="post_surveys")

    # Discussion Quality Scale
    dialogue_management = models.IntegerField()
    information_pooling = models.IntegerField()
    reaching_consensus = models.IntegerField()
    task_division = models.IntegerField()
    time_management = models.IntegerField()
    technical_coordination = models.IntegerField()
    reciprocal_interaction = models.IntegerField()
    individual_task_orientation = models.IntegerField()

    # LLM Usability
    llm_collaboration = models.IntegerField(null=True, blank=True)
    llm_satisfaction = models.IntegerField(null=True, blank=True)
    llm_quality = models.IntegerField(null=True, blank=True)
    llm_recommendation = models.IntegerField(null=True, blank=True)
    llm_future_use = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Post Survey {self._id} from {self.participant._id}"

class PostSurveyLLM(models.Model):
    """Stores each participant's post-survey responses."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="post_surveys_llm")
    # Optional open-ended response
    open_ended_response = models.TextField(null=True, blank=True)

    # Likert scale questions
    llm_summary = models.IntegerField(null=True, blank=True)
    llm_encouragement = models.IntegerField(null=True, blank=True)
    llm_alternatives = models.IntegerField(null=True, blank=True)
    llm_collaboration = models.IntegerField(null=True, blank=True)
    llm_satisfaction = models.IntegerField(null=True, blank=True)
    llm_quality = models.IntegerField(null=True, blank=True)
    llm_recommendation = models.IntegerField(null=True, blank=True)
    llm_future_use = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Post Survey {self._id} from {self.participant._id}"
    
class PostSurveyTask(models.Model):
    """Stores each participant's post-survey responses."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="post_surveys_task")

    # Discussion Quality Scale
    dialogue_management = models.IntegerField()
    information_pooling = models.IntegerField()
    reaching_consensus = models.IntegerField()
    time_management = models.IntegerField()
    reciprocal_interaction = models.IntegerField()
    individual_task_orientation = models.IntegerField()



    def __str__(self):
        return f"Post Survey {self._id} from {self.participant._id}"
    

class PostSurveyNasa(models.Model):
    """Stores each participant's NASA-TLX survey responses."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="post_surveys_task_nasa")

    # NASA-TLX Scales
    mental_demand = models.IntegerField()
    temporal_demand = models.IntegerField()
    performance = models.IntegerField()
    effort = models.IntegerField()
    frustration = models.IntegerField()

    def __str__(self):
        return f"NASA-TLX Survey {self._id} from {self.participant._id}"

class PreSurvey(models.Model):
    """Stores each participant's post-survey responses."""
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="pre_surveys")

    # Pre-survey demographic and knowledge questions
    ai_knowledge = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pre Survey {self._id} from {self.participant._id}"