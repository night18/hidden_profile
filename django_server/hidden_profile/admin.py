from django.contrib import admin
from .models import CandidateProfile, Participant, Group, Condition, Role, Turn, ParticipantTurn, Message, LlmMessage, FormalRecord, InitialRecord, PostSurvey

# Register your models here.
admin.site.register(CandidateProfile)
admin.site.register(Participant)
admin.site.register(Group)
admin.site.register(Condition)
admin.site.register(Role)
admin.site.register(Turn)
admin.site.register(ParticipantTurn)
admin.site.register(Message)
admin.site.register(LlmMessage)
admin.site.register(FormalRecord)
admin.site.register(InitialRecord)
admin.site.register(PostSurvey)
