import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import transaction
import random
from .gpt import OpenAIClient
import datetime
import ast
from datetime import timedelta, timezone
import asyncio
import uuid
from channels.layers import get_channel_layer
import contextlib  
from .models import (
    CandidateProfile, Participant, Group, Role, Turn, ParticipantTurn, Message, LlmMessage, FormalRecord, Condition
)
from .serializers import CandidateProfileSerializer 
TOTAL_TURNS = 1
LLM_START_TIME = 10  # seconds
LLM_IDLE_TIME = 10  # seconds


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Import models here to ensure Django is loaded
        from .models import Group, Participant
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.openai_client = OpenAIClient()
        self.watchdog_flag = False
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        from .models import Group, Participant
        # Check when do they leave the room
        # case 1: leave when pairing
        # case 2: leave after pairing
        # case 3: leave because finish the experiment
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        
        group = await sync_to_async(Group.objects.get)(pk=self.room_name)
        participant = await sync_to_async(Participant.objects.get)(pk=self.participant_id)
        if hasattr(self, "auto_llm_task"):
            self.auto_llm_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.auto_llm_task
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
            self.group_id= participant.group_id
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
                
                # Get the condition of the group
                condition = await sync_to_async(lambda: group.condition._id)()

                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "type": "chat_message",
                        "message": {
                            "type": "room_ready",
                            "participants": participant_info,
                            "condition": condition,
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
            print('message received')
            print(data)
            
            group = await sync_to_async(Group.objects.get)(pk=group_id)
            sender = await sync_to_async(Participant.objects.get)(pk=sender_id)
            turn = await sync_to_async(Turn.objects.get)(group=group, turn_number=turn_number)
            
            # Save the message to the database
            message = await sync_to_async(Message.objects.create)(group=group, sender=sender, turn=turn, content=content)
            message_id = str(message._id)

            # Check the condition id to decide whether and how LLM should respond
            condition_id = await sync_to_async(lambda: group.condition._id)()
            if condition_id == 1 and "@quori" in content.lower():

                await self.channel_layer.send(
                    self.channel_name,
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

            else:
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

            # If the condition id is 1 and @quori is in the message, send the message to the original sender only
            if "@quori" in content.lower() and (condition_id == 1 or condition_id == 2):
                print('@quori detected in the message content')
                # When codition is 1, is_private is True, when condition is 2, is_private is False
                is_private = condition_id == 1
                

                asyncio.create_task(self.quori_response(group, turn, sender, is_private))







        elif type == "complete_initial":
            """
                A signal to indicate that the participant has completed the initial decision. 
                After receive this signal from all participants, the group will be ready to start the experiment.
                Hence, it has to send a signal to all participants to indicate that the experiment is ready to start.
            """
            sender_id = data["sender"]
            turn_number = data["turn_number"]
            self.turn_number = turn_number


            group_id = self.room_name
            turn = await sync_to_async(Turn.objects.get)(group=group_id, turn_number=turn_number)
            self.turn_id= turn._id
            
            # Change the turn start time to current time
            turn.start_time = datetime.datetime.now(datetime.timezone.utc)
            await sync_to_async(turn.save)()

            
            sender = await sync_to_async(Participant.objects.get)(pk=sender_id)
            sender.complete_initial = True
            
            await sync_to_async(sender.save)(update_fields=["complete_initial"])

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

            someone_incomplete = await sync_to_async(
                Participant.objects.filter(group_id=self.room_name,
                                        complete_initial=False).exists
            )()

            group = await sync_to_async(Group.objects.get)(pk=group_id)
            condition_id = await sync_to_async(lambda: group.condition._id)()

            role_map= await self.get_role_alias_dict()
            self.role_map= role_map

            if condition_id == 1:
                # Every participant gets their own LLM task
                print(f"[LLM] Starting individual LLM (condition 1) for participant {self.participant_id}")
                self.auto_llm_task = asyncio.create_task(self.periodic_llm_call(group, turn))



            elif condition_id == 2:
                if someone_incomplete:
                    return 
                self.auto_llm_task = asyncio.create_task(self.periodic_llm_call(group, turn))




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


    async def get_role_alias_dict(self):
        from .models import ParticipantTurn
        queryset = (
            ParticipantTurn.objects
            .filter(turn_id=self.turn_id, participant__group_id=self.group_id)
            .select_related("participant")           # pre-join Participant
        )

        # Evaluate the QS off-thread so the event loop never blocks
        pt_rows = await sync_to_async(list)(queryset)

        role_alias = {}
        for pt in pt_rows:
            if pt.role_id not in role_alias:         # first Participant per role “wins”
                p = pt.participant
                role_alias[pt.role_id] = f"{p.avatar_color} {p.avatar_animal}"

        return role_alias



          
            
    
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))
    
    async def periodic_llm_call(self,group,turn):
        from .models import Participant, ParticipantTurn, Message, LlmMessage

        # Check the group's condition id to decide whether and how LLM should respond
        condition_id = await sync_to_async(lambda: group.condition._id)()
        if condition_id==0:
            return
        last_intervention_analysis=datetime.datetime.now(datetime.timezone.utc)
        turn_number = self.turn_number
        group_id = self.group_id
        sender_id = self.participant_id
        if condition_id == 1:
            participant = await sync_to_async(Participant.objects.get)(pk=sender_id)
            self.participant_alias= participant.avatar_color + " " + participant.avatar_animal
            print(f"[LLM] Starting periodic LLM call for participant {self.participant_alias} in group {group_id} for turn {turn_number}")
            participant_turn=  await sync_to_async(ParticipantTurn.objects.get)(participant=participant,turn=turn)
            role_id= participant_turn.role_id
            self.role_id= role_id
            role_map= await self.get_role_alias_dict()
            self.role_map= role_map
        elif condition_id == 2:
            role_map= await self.get_role_alias_dict()
            self.role_map= role_map
            print(f"[LLM] Starting periodic LLM call for group {group_id} for turn {turn_number}")
        while True:
            await asyncio.sleep(10) # check every second
            message_count = await sync_to_async(
                lambda: Message.objects.filter(group=group, turn=turn).count()
            )()

            # less than 5 messages? → skip the intervention loop iteration
            if message_count < 5:
                continue

            last_message=  await sync_to_async(lambda: Message.objects.filter(group=group, turn=turn).order_by('-timestamp').first())()
            if last_message and (datetime.datetime.now(datetime.timezone.utc) - last_message.timestamp).total_seconds() < 10: #if less time than threshold do not interrupt
                continue
            if (datetime.datetime.now(datetime.timezone.utc) - last_intervention_analysis).total_seconds() < 20:
                continue
            last_intervention_analysis = datetime.datetime.now(datetime.timezone.utc)

            if condition_id == 1:
                # If the time period between the last non summerized LLM message and the current message is less than 30 seconds, do not respond
                last_llm_message = await sync_to_async(lambda: LlmMessage.objects.filter(group=self.group_id, turn=turn_number, is_summary=False).order_by('-timestamp').first())()
                if last_llm_message and (datetime.datetime.now(datetime.timezone.utc) - last_llm_message.timestamp).total_seconds() < LLM_IDLE_TIME:
                    continue


                while True:#use  loop and try in case llm response format is not correct
                    try: 
                        intervention_response, llm_message_id = await self.openai_client.intervention_analyzer_response( group, turn,participant,private=True)                                              
                        print('inter')
                        print(intervention_response)
                        print(self.participant_alias)
                        intervention_response = json.loads(intervention_response)


                    
                        if intervention_response["summarization"]['score'] >= 70:
                            response = await self.openai_client.individual_level_response(participant, group, turn,"Summarization",role_id)
                            type_of_intervention   = "Summarization"
                        elif intervention_response["nudging"]['score']  > 70:
                            response = await self.openai_client.individual_level_response(participant, group, turn,"Nudging",role_id)
                            type_of_intervention = "Nudging"
                        elif intervention_response["devils_advocate"]['score']  >75:
                            response = await self.openai_client.individual_level_response(participant, group, turn,"Devils Advocate",role_id)
                            type_of_intervention = "Devils Advocate"
                        else:
                            # If no intervention is needed, do not respond
                            break
                    except Exception as e:
                        print("LLM error:", e, flush=True)
                        import traceback
                        traceback.print_exc()
                        continue
                    if last_message and (datetime.datetime.now(datetime.timezone.utc) - last_message.timestamp).total_seconds() < 10: #if less time than threshold do not interrupt
                        break # If there was a message before crafting the response dont send the message
                            # Store the response as new data in the database
                    llm_message = await sync_to_async(LlmMessage.objects.create)(
                        group=group, 
                        turn=turn, 
                        content=response, 
                        is_private=True, 
                        recipient=participant,
                        type_of_intervention=type_of_intervention,
                    )
        




                    await self.channel_layer.send(
                        self.channel_name,
                        {
                            "type": "chat_message",
                            "message": {
                                "type": "message",
                                "content": {
                                    "_id": str(llm_message._id),
                                    "sender": {
                                        "participant_id": -1,  
                                    },
                                    "content": response
                                }
                            }
                        }
                    )


            elif condition_id == 2:
                last_llm_message = await sync_to_async(lambda: LlmMessage.objects.filter(group=self.group_id, turn=turn_number, is_summary=False).order_by('-timestamp').first())()
                if last_llm_message and (datetime.datetime.now(datetime.timezone.utc) - last_llm_message.timestamp).total_seconds() < LLM_IDLE_TIME:
                    continue


                while True:#use  loop and try in case llm response format is not correct
                    try: 
                        intervention_response, llm_message_id = await self.openai_client.intervention_analyzer_response( group, turn,None,private=False)                                              
                        print('inter')
                        print(intervention_response)

                        intervention_response = json.loads(intervention_response)


                    
                        if intervention_response["summarization"]['score'] >= 65:
                            response = await self.openai_client.group_level_response( group, turn,"Summarization",role_map)
                            type_of_intervention = "Summarization"
                        elif intervention_response["nudging"]['score']  > 65:
                            response = await self.openai_client.group_level_response( group, turn,"Nudging",role_map)
                            type_of_intervention = "Nudging"
                        elif intervention_response["devils_advocate"]['score']  >70:
                            response = await self.openai_client.group_level_response( group, turn,"Devils Advocate",role_map)
                            type_of_intervention = "Devils Advocate"
                        else:
                            # If no intervention is needed, do not respond
                            break
                    except Exception as e:
                        print("LLM error:", e, flush=True)
                        import traceback
                        traceback.print_exc()
                        continue
                    if last_message and (datetime.datetime.now(datetime.timezone.utc) - last_message.timestamp).total_seconds() < 10: #if less time than threshold do not interrupt
                        break # If there was a message before crafting the response dont send the message
                    # Store the response as new data in the database
                    llm_message=await sync_to_async(LlmMessage.objects.create)(
                        group=group, 
                        turn=turn, 
                        content=response, 
                        is_private=False, 
                        recipient=None,
                        type_of_intervention=type_of_intervention)


                    
                    # Broadcast the LLM response to the group
                    await self.channel_layer.group_send(
                        self.room_name,
                        {
                            "type": "chat_message",
                            "message": {
                                "type": "message",
                                "content": {
                                "_id": str(llm_message._id),
                                "sender": {
                                    "participant_id": -1,  
                                },
                                "content": response
                            }
                            }
                        }
                    )


                
            
    async def quori_response(self, group, turn, participant, private):
        # Get the group
        if private:
            response = await self.openai_client.individual_level_response(participant, group, turn,"Summarization",self.role_id)


            llm_message = await sync_to_async(LlmMessage.objects.create)(
                group=group, 
                turn=turn, 
                content=response, 
                is_private=True, 
                recipient=participant,
                type_of_intervention='Summarization'
            )





            await self.channel_layer.send(
                self.channel_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "message",
                        "content": {
                            "_id": str(llm_message._id),
                            "sender": {
                                "participant_id": -1,  
                            },
                            "content": response
                        }
                    }
                }
            )
        else:
            response = await self.openai_client.group_level_response( group, turn,"Summarization",self.role_map)
            type_of_intervention = "Summarization"


            llm_message=await sync_to_async(LlmMessage.objects.create)(
                group=group, 
                turn=turn, 
                content=response, 
                is_private=False, 
                recipient=None,
                type_of_intervention=type_of_intervention)



            # Broadcast the LLM response to the group
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": {
                        "type": "message",
                        "content": {
                        "_id": str(llm_message._id),
                        "sender": {
                            "participant_id": -1,  
                        },
                        "content": response
                    }
                    }
                }
            )