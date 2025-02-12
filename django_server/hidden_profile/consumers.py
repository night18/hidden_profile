import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import CandidateProfile, Participant, Group, Role, Turn, PariticipantTurn, Message, LlmMessage, FormalRecord, Condition
import random

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
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        
        group = await sync_to_async(Group.objects.get)(pk=self.room_name)
        participant = await sync_to_async(Participant.objects.get)(pk=self.participant_id)
        
        if await sync_to_async(group.is_full)():
            # Case 2
            await sync_to_async(group.remove_participant)(participant)
        else:
            # Case 1
            await sync_to_async(group.remove_participant)(participant)
        
        group_count = await sync_to_async(group.participants.count)()
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": {
                    "type": "user_left",
                    "participant": self.participant_id,
                    "remaining": group.max_size - group_count
                }
            }
        )
        
        
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        print(data)
        type = data["type"]
        print(type)
        
        if type == "join":
            participant_id = data["participant_id"]
            if participant_id is None:
                raise ValueError("Participant ID cannot be None")
            
            self.participant_id = participant_id
            participant = await sync_to_async(Participant.objects.get)(pk=participant_id)
            group_id = participant.group_id
            group = await sync_to_async(Group.objects.get)(pk=group_id)
            await sync_to_async(group.activate_participant)(participant)
            
            group_count = await sync_to_async(group.participants.count)()
            
            
            if group_count == group.max_size:
                
                # Get all participant ids in the group
                participants = await sync_to_async(group.participants.all)()
                participant_ids = [participant.id for participant in participants]
                
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "type": "chat_message",
                        "message": {
                            "type": "room_ready",
                            "participants": participant_ids                            
                        }
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "type": "chat_message",
                        "message": {
                            "type": "waiting",
                            "remaining": group.max_size - group_count
                        }
                    }
                )
        elif type == "candidate_profiles_by_turn":
            """
            For each turn, the participants will be assigned to a different role.
            The whole group would have all the roles.
            The participants will be assigned to the roles in a random order.
            Each participants would see the same pair of candidates but differnt candidate attributes based on their role.
            """
            
            participant_id = data["participant_id"]
            turn = data["turn"]
            
        elif type == "candidate_profiles_by_turn":
            participant_id = data["participant_id"]
            turn = data["turn"]
            
            participant = await sync_to_async(Participant.objects.get)(pk=participant_id)
            group = await sync_to_async(Group.objects.get)(pk=participant.group_id)
            
            # Get all roles and shuffle them
            roles = await sync_to_async(list)(Role.objects.all())
            random.shuffle(roles)
            
            participants = await sync_to_async(list)(group.participants.all())
            
            if len(participants) != len(roles):
                raise ValueError("Number of participants and roles do not match")
            
            # Assign roles to participants
            with transaction.atomic():
                for i, participant in enumerate(participants):
                    role = roles[i]
                    await sync_to_async(ParticipantTurn.objects.create)(
                        participant=participant,
                        turn=turn,
                        role=role
                    )
            
            # Prepare candidate profiles for each participant based on their role
            candidate_profiles = {}
            for participant in participants:
                participant_turn = await sync_to_async(ParticipantTurn.objects.get)(
                    participant=participant,
                    turn=turn
                )
                role = participant_turn.role
                candidate_profiles[participant.id] = await sync_to_async(self.get_candidate_profiles_by_role)(role)
            
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "candidate_profiles_by_turn",
                        "candidate_profiles": candidate_profiles
                    }
                }
            )
            
        
        elif type == "message":
            pass
            
    
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))
                