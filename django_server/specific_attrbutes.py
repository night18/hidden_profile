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
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "llm_public_private_counts.csv")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_distinct_attributes(transcript_text, attributes):
    """
    Sends transcript to LLM and returns a LIST of unique attributes mentioned.
    """
    if not transcript_text.strip():
        return []

    attributes_str = ", ".join(attributes)
    
    prompt = f"""
    Analyze the following transcript of a single participant in a hiring discussion.
    
    From the list of target attributes below, identify WHICH ones are mentioned or referenced by this participant.
    
    Target Attributes: {attributes_str}

    Return ONLY a JSON array containing the names of the attributes that were present.
    Example: ['Funding', 'Interdisciplinarity']
    
    Transcript:
    "{transcript_text}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            response_format={"type": "json_object"}, 
            messages=[
                {"role": "system", "content": "You are a data extractor. Return a valid JSON object with key 'mentioned_attributes' containing a list of strings."},
                {"role": "user", "content": prompt}
            ],
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return data["mentioned_attributes"]
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return []

def main():
    if not OPENAI_API_KEY or "sk-" not in OPENAI_API_KEY:
        print("ERROR: Please set a valid OPENAI_API_KEY in the script.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    groups = Group.objects.select_related('condition').all()
    rows = []

    print(f"Starting analysis for {len(ALL_TARGET_ATTRIBUTES)} attributes across {groups.count()} groups...")

    # Sets for fast lookup
    public_set_ref = set(TARGET_ATTRIBUTES_PUBLIC)
    private_set_ref = set(TARGET_ATTRIBUTES_PRIVATE)
# ...existing code...
    allowed_group_ids = [
        "f5b22edf-83f4-44f3-a20c-a74e70eabe56",
        "5aa46cf5-20d8-4b6e-a321-3531b157329c",
        "3c5d13af-e1ee-4594-b9c3-a1c838d7cd9d",
        "e058be3d-7b2b-4d86-b157-010c2e96c35c",
        "a84800e4-ae47-442d-89f6-28f2b986b939",
        "7414b44a-deaf-49b4-8922-40bc7f713414",
        "c5c60b85-b9d4-421a-9400-162e1e726646",
        "829f2af8-86b1-427d-b181-18f6fd1c8386",
        "390beb41-788f-40ff-80b4-9cbc07ac054d",
        "2821920b-c974-43ca-a21a-cf48fab63463",
        "27e67a5f-8180-48f4-9f52-a8e4ecf1d568",
        "c74231f1-28e6-467c-8fbc-555dca01636e",
        "f615a038-1f63-48b2-9171-a327ac44d16f",
        "bacc75ae-7843-464f-8af6-bcbe175157ad",
        "144e3d7a-55cf-4821-b3c3-6a6d5f8a9f3a",
        "43ecc645-0c1f-42c4-8811-1d328753fdb3",
        "08a44e67-54c7-408e-ae76-4640ae0abc2b",
        "3962bbea-d6c8-4f8e-b745-cd280f27029b",
        "fea7b096-c362-4a76-9e51-49a17b66b0cc",
        "2aa8a462-3958-42b7-8ea9-d6bfde17654e",
        "0628e2bc-278f-4ff5-976b-e6be1416568d",
        "b1518e4a-b267-4ecb-9006-fe5ea17cd661",
        "e1e6ab60-3a2a-46cf-b4e9-f9b7c8ec360c",
        "cd787f8d-5fe8-4437-9492-f96db18ab11a",
        "bf7fc9f7-1bb7-4d51-9780-f430871edb62",
        "f3ab1d88-a6e8-4c0b-b9bf-e991442e3f6d",
        "b309f750-524b-40ae-bc59-65f7bce2497f",
        "edc616f3-4d41-47a7-b992-89cbda804e33",
        "d82bb0c6-2992-48a6-9fef-b9f50095310c",
        "53014f43-d524-4a4e-9964-7f9d83d0568c",
        "239469a8-8d9d-49d5-893f-ee0e48ce8a52",
        "799555e8-5c4a-40a3-84ed-0540f3b314f9",
        "ca3d5412-9e42-40ba-8293-21daf1d05c40",
        "f8df503d-5605-45d5-91a4-7b594bae6a0c",
        "ebabf395-06da-48af-8e8d-9ded46fa4453",
        "2ba13d74-e34c-4abf-a567-efad3f9e42e6",
        "1502f52a-1aa1-4668-a3b4-4d2e63bf61b5",
        "24e93b4c-5e8e-4990-8593-f561275bd496",
        "4398f4c0-7eb4-4569-80d0-d4482ddd2359",
        "ebdcffaa-7a3d-4725-b43f-52143fd84168",
        "6c8939b2-b4f2-47db-ac20-6006494fdc0a",
        "2b629ec9-1182-4dcc-bce9-46a39915fa3d",
        "aa0e5462-6a84-42ae-9ae0-65b7d86621f6",
        "6a509fd9-79ff-4c8b-935b-07e942a75319",
        "54ba19cb-082d-4cd1-be23-c6382022a835",
        "e16db37e-6f83-4179-aadc-5f5def58f33c",
        "c969cd7d-db23-481b-a19d-3f3e567ad667",
        "01ec227f-b8dc-4e0e-9b20-395b7a5c8142"
    ]
# ...existing code...
    for group in groups:
        # --- NEW: Validation Check ---
        # Check if any participant in this group has a missing FormalVote record
        # or if a record exists but the vote is None.
        if str(group._id) not in allowed_group_ids:
            continue

        participants = group.participants.all()
        formal_records_count = FormalRecord.objects.filter(participant__in=participants).count()
        if formal_records_count < 3:
            print(f"Skipping Group {group._id}: Found only {formal_records_count} FormalRecords for Turn 1 (Expected >= 3).")
            continue

        print(f"Processing Group {group._id}...")
        participants = list(group.participants.all().order_by('start_time'))

        # Optional Check 2: Does the group have NO formal records at all? (If this counts as "NA doesn't exist")
        # Uncomment if you want to skip groups that simply haven't reached the voting stage yet.
        # if not FormalRecord.objects.filter(participant__in=participants).exists():
        #    print(f"Skipping Group {group._id}: No FormalRecords found.")
        #    continue
        # -----------------------------

        print(f"Processing Group {group._id}...")
    
        # We also want to track unique mentions for the WHOLE group
        group_public_mentions = set()
        group_private_mentions = set()

        row_data = {
            "group_id": group._id,
            "condition": group.condition.description,
            "difficulty": getattr(group, 'difficulty'),
            "p1_stats": "{}",
            "p2_stats": "{}",
            "p3_stats": "{}",
            "overall_stats": "{}"
        }

        # Iterate max 3 participants
        for i in range(3):

            
            p = participants[i]
            
            # 1. Get Transcript
            messages = Message.objects.filter(group=group, sender=p)
            full_text = "\n".join([m.content for m in messages])
            
            # 2. Get List of Mentioned Attributes from LLM
            mentioned_list = get_distinct_attributes(full_text, ALL_TARGET_ATTRIBUTES)
            mentioned_set = set(mentioned_list)

            # 3. Categorize Counts
            pub_count = len(mentioned_set.intersection(public_set_ref))
            priv_count = len(mentioned_set.intersection(private_set_ref))
            total_count = len(mentioned_set)

            # 4. Store Stats for Participant
            stats = {
                "public": pub_count,
                "private": priv_count,
                "total": total_count
            }
            row_data[f"p{i+1}_stats"] = json.dumps(stats)
            
            # 5. Update Group Sets (to calculate overall distinct later)
            group_public_mentions.update(mentioned_set.intersection(public_set_ref))
            group_private_mentions.update(mentioned_set.intersection(private_set_ref))

        # 6. Calculate Overall Distinct Stats (Union of all participants)
        overall_stats = {
            "public": len(group_public_mentions),
            "private": len(group_private_mentions),
            "total": len(group_public_mentions) + len(group_private_mentions)
        }
        row_data["overall_stats"] = json.dumps(overall_stats)
        
        rows.append(row_data)

    fieldnames = [
        "group_id", "condition", "difficulty",
        "p1_stats", "p2_stats", "p3_stats", 
        "overall_stats"
    ]

    try:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nAnalysis complete. Results saved to: {OUTPUT_CSV}")
    except IOError as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    main()