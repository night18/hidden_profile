from openai import AsyncOpenAI
import os
from asgiref.sync import sync_to_async
import heapq
from .models import Group, Turn, ParticipantTurn, Message, LlmMessage

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "o3-mini-2025-01-31"
        self.max_tokens = 20000
        # Load system prompts and templates at initialization
        self.group_system_prompt = self._load_prompt("group_system_prompt.txt")
        self.individual_system_prompt = self._load_prompt("individual_system_prompt.txt")
        self.individual_system_private_prompt= self._load_prompt("individual_system_prompt_private.txt")
        self.quori_system_prompt = self._load_prompt("quori_system_prompt.txt")
        self.group_summarization_prompt = self._load_prompt("group_summarization_prompt.txt")
        self.intervention_analyzer_prompt = self._load_prompt("intervention_analyzer.txt")
        self.intervention_analyzer_private_prompt = self._load_prompt("intervention_analyzer_private.txt")


    def _load_prompt(self, filename):
        #Helper method to load prompt templates from files
        base_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(base_dir, filename)
        try:
            with open(prompt_path, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    async def generate_response(self, messages):
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_completion_tokens=self.max_tokens,
        )
        print("completion")
        print(completion.choices[0].message.content)


        return completion.choices[0].message.content
    
    def get_participant_alias(self, participant):
        # Get the participant
        return participant.avatar_color + " " + participant.avatar_animal
    
    def get_group_chat_history(self, group_id, turn_number, participant, private):
        from .models import Group, Turn, ParticipantTurn, Message, LlmMessage
        # Get the group
        group = Group.objects.get(pk=group_id)
        
        # Get the turn
        turn = Turn.objects.get(group=group, turn_number=turn_number)
        
        # Get the messages in the group. Sort by timestamp, the older messages come first
        chat_messages = list(Message.objects.filter(group=group, turn=turn,quori_included=False).order_by("timestamp"))
        if private:
            llm_messages = LlmMessage.objects.filter(group=group, turn=turn,recipient=participant,is_intervention_analysis=False).order_by("timestamp")
        else:
            llm_messages = LlmMessage.objects.filter(group=group, turn=turn,is_private=False,is_intervention_analysis=False).order_by("timestamp")
        chat_messages.extend(llm_messages)
        chat_messages.sort(key=lambda m: m.timestamp)

        # Format the messages for the OpenAI API
        formatted_messages = []
        for msg in chat_messages:
            if isinstance(msg, Message):                 # human
                alias = self.get_participant_alias(msg.sender)
                formatted_messages.append(
                    {"role": "user", "content": f"{alias}: {msg.content}"}
                )
            else:                                        # LLM
                formatted_messages.append(
                    {"role": 'assistant', "content": f"Assitant: {msg.content}. (This message was a {msg.type_of_intervention})"}
                )
        
        return formatted_messages


    

    async def individual_level_response(self, participant, group, turn, intervention_type,role_id):
        # Get the participant

        #role_description = turn.role.description
        
        hidden_profile_attributes = ""
        attributes = "Number of Courses Taught, Student Teaching Evaluations, Number of Peer-Reviewed Publications, Citation Impact, Service on Editorial Boards, Conference Organization Roles"
        
        if role_id == 1:
            hidden_profile_attributes = "Undergraduate Mentorship Success, Graduate Thesis Supervision, Curriculum Development, Teaching Awards"
        elif role_id == 2:
            hidden_profile_attributes = "Grant Funding Secured, Impact of Research Publications, Interdisciplinary Research, Research Awards"
        elif role_id == 3:
            hidden_profile_attributes = "Invited Talks, Industry Collaboration, University Committee Service, Diversity and Inclusion Initiatives"
        
        attributes = attributes + ", " + hidden_profile_attributes
        
        messages = []
        system_prompt = self.individual_system_private_prompt.format(
            participant_name=self.get_participant_alias(participant),
            private_information=hidden_profile_attributes,
            shared_information=attributes
        )
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": f"Intervention Type: {intervention_type}"})
        # Get the messages in the group. Sort by timestamp, the older messages come first

        chat_messages = await sync_to_async(self.get_group_chat_history)(group._id, turn.turn_number,participant, private=True)

        messages.extend(chat_messages)
        print("messages")
        print(messages)

        response = await self.generate_response(messages)
        

        return response
    
    async def group_level_response(self, group, turn, intervention_type, role_map):
        # Get the participants in the group

        
        system_prompt = self.group_system_prompt.format(
            role_id_1=role_map[1],
            role_id_2=role_map[2],
            role_id_3=role_map[3],
            public_information="Number of Courses Taught, Student Teaching Evaluations, Number of Peer-Reviewed Publications, Citation Impact, Service on Editorial Boards, Conference Organization Roles",

            )
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        messages.append({"role": "user", "content": f"Intervention Type: {intervention_type}"})

        # Get the messages in the group. Sort by timestamp, the older messages come first
        chat_messages = await sync_to_async(self.get_group_chat_history)(group._id, turn.turn_number,participant=None, private=False)
        messages.extend(chat_messages)
        print("messages")
        print(messages)

        response = await self.generate_response(messages)
        

        
        return response
    async def intervention_analyzer_response(self, group, turn, participant,private=True):
        from .models import LlmMessage
        # Get the group
        if private:#private assistant


            messages = []
            system_prompt = self.intervention_analyzer_private_prompt.format(
                participant_name=self.get_participant_alias(participant)
            )
            messages.append({"role": "system", "content": system_prompt})

        else:
            messages = [
                {"role": "system", "content": self.intervention_analyzer_prompt},
            ]
        
        
        # Get the messages in the group. Sort by timestamp, the older messages come first
        chat_messages = await sync_to_async(self.get_group_chat_history)(group._id, turn.turn_number,participant, private=private)
        messages.extend(chat_messages)



        # Generate the response using the OpenAI API        
        response =await self.generate_response(messages)
        
        # Store the response as new data in the database
        llm_message = await sync_to_async(LlmMessage.objects.create)(
            group=group,
            turn=turn,
            content=response,
            recipient=participant if private else None,
            is_private=private,
            is_intervention_analysis=True,
            input_messages=str(chat_messages)
        )        
        
        return response, llm_message._id