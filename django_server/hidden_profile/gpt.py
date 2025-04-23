from openai import OpenAI
from .models import Group, Turn, ParticipantTurn, Message, LlmMessage, Participant
import os

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        self.max_tokens = 150
        self.group_system_prompt_template = self.load_group_system_prompt_template()
        self.individual_system_prompt_template = self.load_individual_system_prompt_template()

    def load_individual_system_prompt_template(self):
        base_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(base_dir, "individual_system_prompt.txt")
        with open(prompt_path, "r") as file:
            return file.read().strip()

    def load_group_system_prompt_template(self):
        base_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(base_dir, "group_system_prompt.txt")
        with open(prompt_path, "r") as file:
            return file.read().strip()

    def generate_response(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens
        )
        print("completion")
        print(completion)
        return completion.choices[0].message.content
    
    def get_participant_alias(self, participant):
        # Get the participant
        return participant.avatar_color + " " + participant.avatar_animal
    
    def get_group_chat_history(self, group_id, turn_number):
        # Get the group
        group = Group.objects.get(pk=group_id)
        
        # Get the turn
        turn = Turn.objects.get(group=group, turn_number=turn_number)
        
        # Get the messages in the group. Sort by timestamp, the older messages come first
        chat_messages = Message.objects.filter(group=group, turn=turn).order_by("timestamp")
        
        # Format the messages for the OpenAI API
        formatted_messages = []
        for chat_message in chat_messages:
            sender_alias = self.get_participant_alias(chat_message.sender)
            formatted_messages.append({"role": "user", "content": f"{sender_alias}: {chat_message.content}"})
        
        return formatted_messages

    def individual_level_response(self, participant_id, group_id, turn_number):
        # Get the participant
        participant = Participant.objects.get(pk=participant_id)
        
        # Get the group
        group = Group.objects.get(pk=group_id)
        
        # Get the turn
        turn = Turn.objects.get(group=group, turn_number=turn_number)
        
        # Get the role of the participant in the turn
        participant_turn = ParticipantTurn.objects.get(participant=participant, turn=turn)
        role_id = participant_turn.role._id
        role_description = participant_turn.role.description
        
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
        system_prompt = self.individual_system_prompt_template.format(
            participant_name=self.get_participant_alias(participant),
            expertise=role_description,
            attributes=attributes,
            hidden_profile_attributes=hidden_profile_attributes
        )
        messages.append({"role": "system", "content": system_prompt})
        
        
        # Get the messages in the group. Sort by timestamp, the older messages come first
        chat_messages = self.get_group_chat_history(group_id, turn_number)
        messages.extend(chat_messages)
        print("messages")
        print(messages)

        response = self.generate_response(messages)
        
        # Store the response as new data in the database
        llm_message = LlmMessage.objects.create(group=group, turn=turn, content=response, is_private=True, recipient=participant)
        
        return response, str(llm_message._id)
    
    def group_level_response(self, group_id, turn_number):
        # Get the participants in the group
        group = Group.objects.get(pk=group_id)
        participants = group.participants.all()
        role_ids = []
        turn = Turn.objects.get(group=group, turn_number=turn_number)
        
        # Find their roles in the current turn
        for participant in participants:
            participant_turn = ParticipantTurn.objects.get(participant=participant, turn=turn)
            role_ids.append(participant_turn.role._id)
            
            
        # Assgin the role to each participant
        teaching_focus_id = None
        research_focus_id = None
        service_focus_id = None
        
        for participant_id, role_id in zip(participants, role_ids):
            if role_id == 1:
                teaching_focus_id = participant_id
            elif role_id == 2:
                research_focus_id = participant_id
            elif role_id == 3:
                service_focus_id = participant_id
        
        
        system_prompt = self.group_system_prompt_template.format(
            teaching_focus_id=self.get_participant_alias(teaching_focus_id),
            research_focus_id=self.get_participant_alias(research_focus_id),
            service_focus_id=self.get_participant_alias(service_focus_id)
            )
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Get the messages in the group. Sort by timestamp, the older messages come first
        chat_messages = self.get_group_chat_history(group_id, turn_number)
        messages.extend(chat_messages)
        print("messages")
        print(messages)

        response = self.generate_response(messages)
        
        # Store the response as new data in the database
        llm_message = LlmMessage.objects.create(group=group, turn=turn, content=response, is_private=False)
        
        
        return response, llm_message._id