import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import CandidateProfile, Participant, Group, Role, Turn, PariticipantTurn, Message, LlmMessage, FormalRecord, Condition

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        
        print('connected to room: ', self.room_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        
        # Check when do they leave the room
        # case 1: leave when pairing
        # case 2: leave after pairing
        await self.channel_layer.group_discard(self.room_name)
        
        group = Group.objects.get(pk=self.room_name)
        participant = Participant.objects.get(pk=self.participant_id)
        
        if group.is_full():
            # Case 2
            group.inactivate_participant(participant)
            response = {
                "code": "user_left",
                
            }
        else:
            # Case 1
            group.remove_participant(participant)
        
        
        
        
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        type = data["type"]
        
        if type == "join":
            participant_id = data["subject_id"]
            if participant_id is None:
                raise ValueError("Participant ID cannot be None")
            
            self.participant_id = participant_id
        
        elif type == "message":
            pass
            
            
            
                