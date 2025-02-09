from django.contrib import admin
from .models import CandidateProfile, Participant, Group, Role, Turn, PariticipantTurn, Message, LlmMessage, FormalRecord

# Register your models here.
admin.site.register(CandidateProfile)
admin.site.register(Participant)
admin.site.register(Group)
admin.site.register(Role)
admin.site.register(Turn)
admin.site.register(PariticipantTurn)
admin.site.register(Message)
admin.site.register(LlmMessage)
admin.site.register(FormalRecord)
