from openai import OpenAI
from .models import Group, Turn, ParticipantTurn, Message, LlmMessage
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
        return(completion.choices[0].message)
    
    def group_level_response(self, group_id, turn_number):
        # Get the participants in the group
        group = Group.objects.get(pk=group_id)
        participants = group.participants.all()
        role_ids = []
        participant_ids = []
        turn = Turn.objects.get(group=group, turn_number=turn_number)
        
        # Find their roles in the current turn
        for participant in participants:
            participant_turn = ParticipantTurn.objects.get(participant=participant, turn=turn)
            role_ids.append(participant_turn.role._id)
            participant_ids.append(participant._id)
            
        # Assgin the role to each participant
        teaching_focus_id = None
        research_focus_id = None
        service_focus_id = None
        
        for participant_id, role_id in zip(participant_ids, role_ids):
            if role_id == 1:
                teaching_focus_id = participant_id
            elif role_id == 2:
                research_focus_id = participant_id
            elif role_id == 3:
                service_focus_id = participant_id
        
        
        system_prompt = self.group_system_prompt_template.format(teaching_focus_id=teaching_focus_id, research_focus_id=research_focus_id, service_focus_id=service_focus_id)
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Get the messages in the group. Sort by timestamp, the older messages come first
        chat_messages = Message.objects.filter(group=group, turn=turn).order_by("timestamp")
        for chat_message in chat_messages:
            messages.append({"role": "user", "content": str(chat_message.sender._id) + ":" + chat_message.content})
        
        response = self.generate_response(messages).content
        
        # Store the response as new data in the database
        llm_message = LlmMessage.objects.create(group=group, turn=turn, content=response, is_private=False)
        
        
        return response, llm_message._id