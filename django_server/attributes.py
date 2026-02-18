import os
import django
import csv
import json

# ---- Bootstrap Django ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "group.settings")
django.setup()

from hidden_profile.models import Group, Message, FormalRecord
from openai import OpenAI

# ---- CONFIGURATION ----

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-proj-...") 

# Attributes categorized
TARGET_ATTRIBUTES_PUBLIC = [
    'Publications', 'Citations', 'Editorial Service', 'Conference Organization'
]
TARGET_ATTRIBUTES_PRIVATE = [
    'Funding', 'Interdisciplinarity', 'Collaborations', 'Research Coverage', 'Mentorship', 'Teaching'
]

# Combined list for the LLM prompt
ALL_TARGET_ATTRIBUTES = TARGET_ATTRIBUTES_PUBLIC + TARGET_ATTRIBUTES_PRIVATE

OUTPUT_DIR = "analysis_results"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "llm_granular_attributes_analysis.csv")

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_granular_attributes(transcript_text, attributes, participant_names):
    """
    Sends transcript to LLM.
    Expects a JSON structure:
    {
      "Participant Name": {
         "Candidate A": ["Attr1", ...],
         "Candidate B": [],
         "Candidate C": []
      },
      ...
    }
    """
    if not transcript_text.strip():
        return {}

    attributes_str = ", ".join(attributes)
    participants_str = ", ".join(participant_names)
    
    prompt = f"""
    Analyze the following group transcript regarding a hiring decision for Candidates A, B, and C.
    
    For EACH participant ({participants_str}), identify which specific attributes they mentioned for EACH Candidate.
    
    Target Attributes to look for: {attributes_str}

    Return a JSON object structured exactly like this:
    {{
      "Participant Name": {{
         "Candidate A": ["Attribute Name", "Attribute Name"],
         "Candidate B": [],
         "Candidate C": ["Attribute Name"]
      }},
      ...
    }}
    Transcript:
    "{transcript_text}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            response_format={"type": "json_object"}, 
            messages=[
                {"role": "system", "content": "You are a precise data extractor. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {}

def calculate_counts(mentioned_list, public_set, private_set):
    """Helper to count public vs private mentions from a list of strings."""
    unique_mentions = set(mentioned_list)
    pub_count = len([m for m in unique_mentions if m in public_set])
    priv_count = len([m for m in unique_mentions if m in private_set])
    return pub_count, priv_count, unique_mentions

def main():
    if not OPENAI_API_KEY or "sk-" not in OPENAI_API_KEY:
        print("ERROR: Please set a valid OPENAI_API_KEY in the script.")
        # return # uncomment if strictly enforcing locally

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    groups = Group.objects.select_related('condition').all()
    
    # Sets for fast lookup
    public_set_ref = set(TARGET_ATTRIBUTES_PUBLIC)
    private_set_ref = set(TARGET_ATTRIBUTES_PRIVATE)

    allowed_group_ids = [
    "01ec227f-b8dc-4e0e-9b20-395b7a5c8142",
    "01ec227f-b8dc-4e0e-9b20-395b7a5c8142ew",
    "03b4abde-3a7d-4d51-b3fb-92b8b4e54635",
    "0628e2bc-278f-4ff5-976b-e6be1416568d",
    "08a44e67-54c7-408e-ae76-4640ae0abc2b",
    "0bdf7663-fe80-4e02-8862-96bd9d72323b",
    "144e3d7a-55cf-4821-b3c3-6a6d5f8a9f3a",
    "1502f52a-1aa1-4668-a3b4-4d2e63bf61b5",
    "239469a8-8d9d-49d5-893f-ee0e48ce8a52",
    "24e93b4c-5e8e-4990-8593-f561275bd496",
    "27e67a5f-8180-48f4-9f52-a8e4ecf1d568",
    "27e67a5f-8180-48f4-9f52-a8e4ecf1d568ew",
    "2821920b-c974-43ca-a21a-cf48fab63463",
    "2a76a40a-10b0-486d-8de1-9be5604dd81f",
    "2aa8a462-3958-42b7-8ea9-d6bfde17654e",
    "2b629ec9-1182-4dcc-bce9-46a39915fa3d",
    "2ba13d74-e34c-4abf-a567-efad3f9e42e6",
    "390beb41-788f-40ff-80b4-9cbc07ac054d",
    "390beb41-788f-40ff-80b4-9cbc07ac054d124",
    "3962bbea-d6c8-4f8e-b745-cd280f27029b",
    "3c5d13af-e1ee-4594-b9c3-a1c838d7cd9d",
    "3c5d13af-e1ee-4594-b9c3-a1c838d7cd9dwed",
    "4398f4c0-7eb4-4569-80d0-d4482ddd2359",
    "43ecc645-0c1f-42c4-8811-1d328753fdb3",
    "53014f43-d524-4a4e-9964-7f9d83d0568c",
    "54ba19cb-082d-4cd1-be23-c6382022a835",
    "5aa46cf5-20d8-4b6e-a321-3531b157329c",
    "6a509fd9-79ff-4c8b-935b-07e942a75319",
    "6c8939b2-b4f2-47db-ac20-6006494fdc0a",
    "7414b44a-deaf-49b4-8922-40bc7f713414",
    "799555e8-5c4a-40a3-84ed-0540f3b314f9",
    "829f2af8-86b1-427d-b181-18f6fd1c8386",
    "a7955733-7fe1-42fc-aaa9-ea6bd81aa4c0",
    "a7955733-7fe1-42fc-aaa9-ea6bd81aa4c0we",
    "a84800e4-ae47-442d-89f6-28f2b986b939",
    "aa0e5462-6a84-42ae-9ae0-65b7d86621f6",
    "adc68378-ade7-49c9-b660-ce7199d4ca09",
    "b1518e4a-b267-4ecb-9006-fe5ea17cd661",
    "bacc75ae-7843-464f-8af6-bcbe175157ad",
    "bf7fc9f7-1bb7-4d51-9780-f430871edb62",
    "c5c60b85-b9d4-421a-9400-162e1e726646",
    "c74231f1-28e6-467c-8fbc-555dca01636e",
    "c969cd7d-db23-481b-a19d-3f3e567ad667",
    "c969cd7d-db23-481b-a19d-3f3e567ad667ew",
    "ca3d5412-9e42-40ba-8293-21daf1d05c40",
    "cd787f8d-5fe8-4437-9492-f96db18ab11a",
    "d82bb0c6-2992-48a6-9fef-b9f50095310c",
    "e058be3d-7b2b-4d86-b157-010c2e96c35c",
    "e16db37e-6f83-4179-aadc-5f5def58f33c",
    "e1e6ab60-3a2a-46cf-b4e9-f9b7c8ec360c",
    "ebabf395-06da-48af-8e8d-9ded46fa4453",
    "ebdcffaa-7a3d-4725-b43f-52143fd84168",
    "edc616f3-4d41-47a7-b992-89cbda804e33",
    "f165c55d-a3a4-413d-8f02-c46dc8b520bf",
    "f3ab1d88-a6e8-4c0b-b9bf-e991442e3f6d",
    "f5b22edf-83f4-44f3-a20c-a74e70eabe56",
    "f615a038-1f63-48b2-9171-a327ac44d16f",
    "f8df503d-5605-45d5-91a4-7b594bae6a0c",
    "fea7b096-c362-4a76-9e51-49a17b66b0cc"
    ]

    # --- DEFINE FIELDNAMES UP FRONT ---
    fieldnames = ["group_id", "condition", "difficulty", "response_data"]
    # Add consensus columns to fieldnames
    fieldnames.append("consensus_A")
    fieldnames.append("majority_A")

    for i in range(1, 4):
        fieldnames.append(f"p{i}_formal_vote") # Formal vote column
        fieldnames.append(f"p{i}_is_vote_A")   # Binary helper
        for c in ["CandidateA", "CandidateB", "CandidateC"]:
            fieldnames.append(f"p{i}_{c}_public")
            fieldnames.append(f"p{i}_{c}_private")
        fieldnames.append(f"p{i}_total_public")
        fieldnames.append(f"p{i}_total_private")
    fieldnames.append("group_overall_public")
    fieldnames.append("group_overall_private")

    # --- CHECK FOR EXISTING PROCESSED GROUPS ---
    processed_ids = set()
    file_exists = os.path.exists(OUTPUT_CSV)
    
    if file_exists:
        try:
            with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'group_id' in row:
                        processed_ids.add(row['group_id'])
            print(f"File {OUTPUT_CSV} exists. Found {len(processed_ids)} processed groups.")
        except Exception as e:
            print(f"Warning could not access existing file: {e}")

    print(f"Starting granular analysis for remaining groups...")
    
    # --- OPEN FILE (APPEND 'a' if exists, WRITE 'w' if new) ---
    mode = 'a' if file_exists else 'w'
    
    try:
        with open(OUTPUT_CSV, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # If we are creating a new file, write header
            if mode == 'w':
                writer.writeheader()
            
            for group in groups:
                # 1. Filter: Allowed List
                if str(group._id) not in allowed_group_ids:
                    continue
                
                # 2. Filter: Already Processed
                if str(group._id) in processed_ids:
                    continue

                participants = list(group.participants.all().order_by('start_time'))
                if len(participants) < 3:
                    formal_count = FormalRecord.objects.filter(participant__in=participants).count()
                    if formal_count < 3:
                        continue

                print(f"Processing Group {group._id}...")

                # 3. Build Transcript
                messages = Message.objects.filter(group=group).select_related('sender').order_by('timestamp')
                transcript_lines = []
                participant_names = [f"{p.avatar_color} {p.avatar_animal}" for p in participants]
                
                for m in messages:
                    sender_label = f"{m.sender.avatar_color} {m.sender.avatar_animal}"
                    transcript_lines.append(f"{sender_label}: {m.content}")
                
                full_transcript = "\n".join(transcript_lines)
                
                # 4. Extract Data
                llm_data = extract_granular_attributes(full_transcript, ALL_TARGET_ATTRIBUTES, participant_names)
                
                # 5. Construct Row
                row = {
                    "group_id": group._id,
                    "condition": group.condition.description,
                    "difficulty": getattr(group, 'difficulty', 'N/A'),
                    "response_data": json.dumps(llm_data)  
                }

                group_all_mentions = set()
                votes_for_A_count = 0 
                
                for i, p in enumerate(participants[:3]): 
                    p_prefix = f"p{i+1}"
                    p_name = participant_names[i]
                    p_data = llm_data.get(p_name, {})
                    p_total_mentions_for_sum = set()

                    # --- Fetch Last Formal Vote ---
                    formal_record = FormalRecord.objects.filter(participant=p).select_related('vote').order_by('-timestamp').first()
                    vote_val = formal_record.vote.name if (formal_record and formal_record.vote) else "N/A"
                    row[f"{p_prefix}_formal_vote"] = vote_val
                    
                    # --- Check if vote is A --
                    is_A = 1 if vote_val == "Candidate A" else 0
                    row[f"{p_prefix}_is_vote_A"] = is_A
                    if is_A:
                        votes_for_A_count += 1

                    for cand in ['Candidate A', 'Candidate B', 'Candidate C']:
                        cand_key = cand.replace(" ", "")
                        mentions = p_data.get(cand, [])
                        pub, priv, unique_set = calculate_counts(mentions, public_set_ref, private_set_ref)
                        
                        row[f"{p_prefix}_{cand_key}_public"] = pub
                        row[f"{p_prefix}_{cand_key}_private"] = priv
                        
                        p_total_mentions_for_sum.update(unique_set)
                        group_all_mentions.update(unique_set)

                    # Aggregate for Participant Overall
                    pub_total, priv_total, _ = calculate_counts(list(p_total_mentions_for_sum), public_set_ref, private_set_ref)
                    row[f"{p_prefix}_total_public"] = pub_total
                    row[f"{p_prefix}_total_private"] = priv_total

                # 6. Group Overall Stats (Consensus / Majority)
                row["consensus_A"] = 1 if votes_for_A_count == 3 else 0
                row["majority_A"] = 1 if votes_for_A_count >= 2 else 0

                g_pub, g_priv, _ = calculate_counts(list(group_all_mentions), public_set_ref, private_set_ref)
                row["group_overall_public"] = g_pub
                row["group_overall_private"] = g_priv
                
                # 7. Write Row Immediately (Save Progress)
                writer.writerow(row)
                csvfile.flush()

        print(f"\nAnalysis complete. Results updated in: {OUTPUT_CSV}")

    except IOError as e:
        print(f"Error accessing CSV: {e}")

if __name__ == "__main__":
    main()