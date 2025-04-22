import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import transaction
from .models import CandidateProfile, Participant, Group, Role, Turn, ParticipantTurn, Message, LlmMessage, FormalRecord, Condition
from .serializers import CandidateProfileSerializer
import random
from .gpt import OpenAIClient

TOTAL_TURNS = 1

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.openai_client = OpenAIClient()
        
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        
        # Check when do they leave the room
        # case 1: leave when pairing
        # case 2: leave after pairing
        # case 3: leave because finish the experiment
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        
        group = await sync_to_async(Group.objects.get)(pk=self.room_name)
        participant = await sync_to_async(Participant.objects.get)(pk=self.participant_id)
        
        if close_code == 4000:
            pass
        elif await sync_to_async(group.is_full)():
            # Case 2
            await sync_to_async(group.inactivate_participant)(participant)
            group_count = await sync_to_async(group.participants.count)()
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "user_left_after_pairing",
                        "participant_id": self.participant_id,
                        "remaining": group.max_size - group_count
                    }
                }
            )
            
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
                        "participant_id": self.participant_id,
                        "remaining": group.max_size - group_count
                    }
                }
            )
        
        
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        type = data["type"]
        
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
                participants = await sync_to_async(list)(group.participants.all())
                participant_info = await sync_to_async(lambda: [
                    {
                        "_id": str(participant._id),
                        "avatar_color": participant.avatar_color,
                        "avatar_animal": participant.avatar_animal,
                    } for participant in participants
                ])()
                
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "type": "chat_message",
                        "message": {
                            "type": "room_ready",
                            "participants": participant_info,
                            "total_turns": TOTAL_TURNS
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
        elif type == "role_by_turn":
            turn_number = data["turn_number"]
            group_id = self.room_name
            
            group = await sync_to_async(Group.objects.get)(pk=group_id)
            participants = await sync_to_async(list)(group.participants.all())
            
            # In the turn has not create, create a new turn
            if not await sync_to_async(Turn.objects.filter(group=group, turn_number=turn_number).exists)():
                turn = await sync_to_async(Turn.objects.create)(group=group, turn_number=turn_number)
            
            # Assign the role to each participant
            roles = await sync_to_async(list)(Role.objects.all())
            random.shuffle(roles)
            
            # Check the number of participants matches the number of roles
            if len(participants) != len(roles):
                raise ValueError("Number of participants must match the number of roles")

            for i, participant in enumerate(participants):
                role = roles[i]
                await sync_to_async(ParticipantTurn.objects.create)(participant=participant, turn=turn, role=role)
            
            # Send the all role-participant pairs to the group
            role_participant_pairs = await sync_to_async(list)(ParticipantTurn.objects.filter(turn=turn))
            
            # use sync_to_async to create pairs of participant, role, and role description
            pairs = await sync_to_async(lambda: [
                {
                    "participant": str(pair.participant._id),
                    "role": pair.role._id,
                    "role_desc": pair.role.description
                } for pair in role_participant_pairs
            ])()
            
            
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "role_assignment",
                        "pairs": pairs
                    }
                }
            )
            
            
        
        elif type == "message":
            """
                Recive
                "type": "message",
                "sender": participantStore.participant_id,
                "turn_number": turnStore.turn_number,
                "content": send_out_message.value
            """
            sender_id = data["sender"]
            content = data["content"]
            turn_number = data["turn_number"]
            group_id = self.room_name
            
            group = await sync_to_async(Group.objects.get)(pk=group_id)
            sender = await sync_to_async(Participant.objects.get)(pk=sender_id)
            turn = await sync_to_async(Turn.objects.get)(group=group, turn_number=turn_number)
            
            # Save the message to the database
            message = await sync_to_async(Message.objects.create)(group=group, sender=sender, turn=turn, content=content)
            message_id = str(message._id)
            
            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "message",
                        "content": {
                            "_id": message_id,
                            "sender": {
                                "participant_id": sender_id,  
                            },
                            "content": content
                        }
                    }
                }
            )

        elif type == "complete_initial":
            """
                A signal to indicate that the participant has completed the initial decision. 
                After receive this signal from all participants, the group will be ready to start the experiment.
                Hence, it has to send a signal to all participants to indicate that the experiment is ready to start.
            """
            sender_id = data["sender"]
            turn_number = data["turn_number"]
            group_id = self.room_name
            

            # send the signal to the groups
            group = await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "complete_initial",
                        "sender": sender_id,
                        "turn_number": turn_number
                    }
                }
            )

        elif type == "ready_to_vote":
            sender_id = data["sender"]
            turn_number = data["turn_number"]
            group_id = self.room_name

            # send the signal to the groups
            group = await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "ready_to_vote",
                        "sender": sender_id,
                        "turn_number": turn_number
                    }
                }
            )

        elif type == "complete_final":
            sender_id = data["sender"]
            turn_number = data["turn_number"]
            group_id = self.room_name
            # send the signal to the groups
            group = await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "complete_final",
                        "sender": sender_id,
                        "turn_number": turn_number
                    }
                }
            )
            

        elif type == "auto_llm":
            """
                Recive
                "type": "auto_llm",
                "sender": participantStore.participant_id,
                "turn_number": turnStore.turn_number,
                "content": send_out_message.value
            """
            sender_id = data["sender"]
            content = data["content"]
            turn_number = data["turn_number"]
            group_id = self.room_name
            print("Auto LLM")
            
            group = await sync_to_async(Group.objects.get)(pk=group_id)
            sender = await sync_to_async(Participant.objects.get)(pk=sender_id)
            turn = await sync_to_async(Turn.objects.get)(group=group, turn_number=turn_number)
            
            # Check the group's condition id to decide whether and how LLM should respond
            condition_id = await sync_to_async(lambda: group.condition._id)()
            if condition_id == 1:
                response, llm_message_id = await sync_to_async(self.openai_client.individual_level_response)(sender_id, group_id, turn_number)
                
                # Send the message to the original sender only
                await self.channel_layer.send(
                    self.channel_name,
                    {
                        "type": "chat_message",
                        "message": {
                            "type": "message",
                            "content": {
                                "_id": str(llm_message_id),
                                "sender": {
                                    "participant_id": -1,  
                                },
                                "content": response
                            }
                        }
                    }
                )
                
            
            elif condition_id == 2:
                # Call the GPT-4o model to generate a response
                
                response, llm_message_id = await sync_to_async(self.openai_client.group_level_response)(group_id, turn_number)
                
                # Broadcast the LLM response to the group
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "type": "chat_message",
                        "message": {
                            "type": "message",
                            "content": {
                            "_id": str(llm_message_id),
                            "sender": {
                                "participant_id": -1,  
                            },
                            "content": response
                        }
                        }
                    }
                )
            
            
    
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))
                