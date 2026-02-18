import os
import django
import csv
from itertools import chain
from datetime import datetime
from collections import Counter

# ---- Bootstrap Django ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "group.settings")  # <-- change this
django.setup()

from django.db.models import Value, CharField, F, Count, Max
from hidden_profile.models import Group, Participant, Message, LlmMessage, PostSurveyLLM, PostSurveyTask, PostSurveyNasa, InitialRecord, FormalRecord, Turn

# ---- ReportLab imports ----
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def to_color(s: str, default=colors.black):
    if not s:
        return default
    s = s.strip()
    if s.startswith("#") and len(s) in (4, 7):
        try:
            return colors.HexColor(s)
        except Exception:
            return default
    key = s.lower().replace(" ", "")
    try:
        return colors.toColor(key)
    except Exception:
        basic = {
            "red": colors.red, "blue": colors.blue, "green": colors.green,
            "purple": colors.purple, "orange": colors.orange, "yellow": colors.yellow,
            "black": colors.black, "gray": colors.gray, "grey": colors.gray,
            "pink": colors.pink, "cyan": colors.cyan, "magenta": colors.magenta,
            "teal": colors.teal, "navy": colors.navy,
        }
        return basic.get(key, default)


def get_transcript_for_participant(participant: Participant):
    group_id = participant.group_id

    human_msgs = (
        Message.objects.filter(group_id=group_id)
        .select_related("sender", "turn")
        .values(
            "_id", "timestamp", "content",
            "turn__turn_number",
            avatar_color=F("sender__avatar_color"),
            avatar_animal=F("sender__avatar_animal"),
        )
        .annotate(source=Value("human", output_field=CharField()))
    )

    public_llm_msgs = (
        LlmMessage.objects.filter(group_id=group_id, is_private=False)
        .select_related("turn")
        .values("_id", "timestamp", "content", "turn__turn_number", "is_intervention_analysis")
        .annotate(source=Value("llm_public", output_field=CharField()))
    )

    private_llm_msgs = (
        LlmMessage.objects.filter(group_id=group_id, is_private=True, recipient=participant)
        .select_related("turn")
        .values("_id", "timestamp", "content", "turn__turn_number", "is_intervention_analysis")
        .annotate(source=Value("llm_private", output_field=CharField()))
    )

    entries = []
    for m in chain(human_msgs, public_llm_msgs, private_llm_msgs):
        if m["source"] == "human":
            sender_label = f"{m.get('avatar_color') or ''} {m.get('avatar_animal') or ''}".strip()
            sender_color = to_color(m.get("avatar_color"), default=colors.black)
            is_intervention = False
        else:
            sender_label = "LLM"
            sender_color = colors.darkblue
            is_intervention = bool(m.get("is_intervention_analysis", False))

        entries.append({
            "message_id": str(m["_id"]),
            "timestamp": m["timestamp"],
            "turn_number": m["turn__turn_number"],
            "sender_label": sender_label or "participant",
            "sender_color": sender_color,
            "content": m["content"],
            "source": m["source"],
            "is_intervention": is_intervention,
        })

    entries.sort(key=lambda x: x["timestamp"])
    return entries

def build_pdf_for_participant(group: Group, participant: Participant, transcript, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, f"{participant._id}.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    styles = getSampleStyleSheet()

    # Styles
    title_style = ParagraphStyle("Title", parent=styles["Title"], alignment=1)
    meta_style = ParagraphStyle("Meta", parent=styles["Normal"], textColor=colors.grey, fontSize=9, leading=12)
    header_style = ParagraphStyle("Header", parent=styles["Normal"], fontName="Helvetica-Bold", leading=14)
    content_style = ParagraphStyle("Content", parent=styles["Normal"], leading=14)
    vote_style = ParagraphStyle("Vote", parent=styles["Normal"], leading=12, leftIndent=12)


    story = []
    # Title
    story.append(Paragraph("Experiment Transcript", title_style))
    story.append(Spacer(1, 6))

    # Get non-intervention LLM message count
    public_llm_count = LlmMessage.objects.filter(
        group=group, is_private=False, is_intervention_analysis=False
    ).count()
    private_llm_count = LlmMessage.objects.filter(
        group=group, recipient=participant, is_private=True, is_intervention_analysis=False
    ).count()
    llm_message_count = public_llm_count + private_llm_count

    difficulty = getattr(group, 'difficulty', 'N/A')
    story.append(Paragraph(f"Group: {group._id}", meta_style))
    story.append(Paragraph(f"Condition: {group.condition._id} - {group.condition.description}", meta_style))
    story.append(Paragraph(f"Difficulty: {difficulty}", meta_style))
    story.append(Paragraph(f"Total LLM Messages (non-intervention): {llm_message_count}", meta_style))
    story.append(Paragraph(f"This PDF is for participant: {participant.avatar_color} {participant.avatar_animal}", meta_style))
    story.append(Spacer(1, 12))

    # --- NEW: Add Group Voting Summary at the top ---
    story.append(Paragraph("Group Voting Summary", header_style))
    turns = group.turns.all().order_by('turn_number')
    teammates = list(group.participants.all().order_by('start_time'))

    if not turns.exists():
        story.append(Paragraph("No voting turns were recorded for this group.", content_style))
    else:
        for turn in turns:
            story.append(Paragraph(f"<b>Turn {turn.turn_number}</b>", content_style))
            for p in teammates:
                initial_vote_str = "N/A"
                formal_vote_str = "N/A"

                initial_record = InitialRecord.objects.filter(participant=p, turn=turn).select_related('vote').first()
                if initial_record and initial_record.vote:
                    initial_vote_str = initial_record.vote.name

                formal_record = FormalRecord.objects.filter(participant=p, turn=turn).select_related('vote').first()
                if formal_record and formal_record.vote:
                    formal_vote_str = formal_record.vote.name
                
                participant_label = f"{p.avatar_color} {p.avatar_animal}"
                vote_paragraph_text = f"<b>{participant_label}:</b> Initial: {initial_vote_str} | Formal: {formal_vote_str}"
                story.append(Paragraph(vote_paragraph_text, vote_style))
            story.append(Spacer(1, 6))
    story.append(Spacer(1, 12))
    story.append(Paragraph("--- Chat Transcript ---", header_style))
    story.append(Spacer(1, 12))
    # Render each message
    for m in transcript:
        ts = m["timestamp"]

        # Only show time (HH:MM:SS); never show a date
        def _only_time(x):
            try:
                return x.strftime("%H:%M:%S")
            except Exception:
                return ""  # if it's not a datetime, omit time entirely to avoid showing a date-like string

        time_str = _only_time(ts)

        header_colored = ParagraphStyle(
            f"Header_{m['message_id']}", parent=header_style, textColor=m["sender_color"]
        )

        # Build header without any date; include time only if available
        prefix = f"[{time_str}] " if time_str else ""
        header_text = f"{prefix}(Turn {m['turn_number']}) <b>{m['sender_label']}</b>"
        story.append(Paragraph(header_text, header_colored))

        story.append(Paragraph(m["content"].replace("\n", "<br/>"), content_style))
        story.append(Spacer(1, 8))

    # Add PostSurveyLLM results
    try:
        post_survey_llm = participant.post_surveys_llm.first()
        if post_survey_llm:
            story.append(Paragraph("LLM Usability", header_style))
            story.append(Paragraph(f"LLM Summary: {post_survey_llm.llm_summary}", content_style))
            story.append(Paragraph(f"LLM Encouragement: {post_survey_llm.llm_encouragement}", content_style))
            story.append(Paragraph(f"LLM Alternatives: {post_survey_llm.llm_alternatives}", content_style))
            story.append(Paragraph(f"LLM Collaboration: {post_survey_llm.llm_collaboration}", content_style))
            story.append(Paragraph(f"LLM Satisfaction: {post_survey_llm.llm_satisfaction}", content_style))
            story.append(Paragraph(f"LLM Quality: {post_survey_llm.llm_quality}", content_style))
            story.append(Paragraph(f"LLM Recommendation: {post_survey_llm.llm_recommendation}", content_style))
            story.append(Paragraph(f"LLM Future Use: {post_survey_llm.llm_future_use}", content_style))
            if post_survey_llm.open_ended_response:
                story.append(Paragraph(f"Open-Ended Response: {post_survey_llm.open_ended_response}", content_style))
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No LLM post-survey data available for this participant.", content_style))
    except Exception as e:
        story.append(Paragraph(f"Error retrieving LLM post-survey data: {e}", content_style))

    # Add PostSurveyTask results
    try:
        post_survey_task = participant.post_surveys_task.first()
        if post_survey_task:
            story.append(Paragraph("Task Feedback", header_style))
            story.append(Paragraph(f"Dialogue Management: {post_survey_task.dialogue_management}", content_style))
            story.append(Paragraph(f"Information Pooling: {post_survey_task.information_pooling}", content_style))
            story.append(Paragraph(f"Reaching Consensus: {post_survey_task.reaching_consensus}", content_style))
            story.append(Paragraph(f"Time Management: {post_survey_task.time_management}", content_style))
            story.append(Paragraph(f"Reciprocal Interaction: {post_survey_task.reciprocal_interaction}", content_style))
            story.append(Paragraph(f"Individual Task Orientation: {post_survey_task.individual_task_orientation}", content_style))
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No task post-survey data available for this participant.", content_style))
    except Exception as e:
        story.append(Paragraph(f"Error retrieving task post-survey data: {e}", content_style))

    # Add PostSurveyNasa results
    try:
        post_survey_nasa = participant.post_surveys_task_nasa.first()
        if post_survey_nasa:
            story.append(Paragraph("NASA TLX (Task Load Index)", header_style))
            story.append(Paragraph(f"Mental Demand: {post_survey_nasa.mental_demand}", content_style))
            story.append(Paragraph(f"Temporal Demand: {post_survey_nasa.temporal_demand}", content_style))
            story.append(Paragraph(f"Performance: {post_survey_nasa.performance}", content_style))
            story.append(Paragraph(f"Effort: {post_survey_nasa.effort}", content_style))
            story.append(Paragraph(f"Frustration: {post_survey_nasa.frustration}", content_style))
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No NASA TLX post-survey data available for this participant.", content_style))
    except Exception as e:
        story.append(Paragraph(f"Error retrieving NASA TLX post-survey data: {e}", content_style))

    doc.build(story)
    return pdf_path

def get_group_stats(group: Group):
    """Calculates and returns a dictionary of statistics for a given group."""
    stats = {
        "group_id": str(group._id),
        "condition_id": group.condition._id,
        "condition_description": group.condition.description,
        "difficulty": getattr(group, 'difficulty', 'N/A'),
        "created_at": group.created_at.strftime("%Y-%m-%d %H:%M:%S") if group.created_at else ''
    }

    # Message counts
    participants = list(group.participants.all().order_by('start_time'))
    stats["total_messages"] = Message.objects.filter(group=group).count()
    stats["llm_messages_intervention"] = LlmMessage.objects.filter(group=group, is_intervention_analysis=False).count()
    stats["llm_messages_analysis_count"] = LlmMessage.objects.filter(group=group, is_intervention_analysis=True).count()
    
    # Vote counts
    stats['initial_vote_A_count'] = InitialRecord.objects.filter(
        participant__in=participants, 
        vote__name='Candidate A'
    ).count()
    
    # Formal Votes (A, B, C)
    stats['formal_vote_A_count'] = FormalRecord.objects.filter(
        participant__in=participants, 
        vote__name='Candidate A'
    ).count()
    stats['formal_vote_B_count'] = FormalRecord.objects.filter(
        participant__in=participants, 
        vote__name='Candidate B'
    ).count()
    stats['formal_vote_C_count'] = FormalRecord.objects.filter(
        participant__in=participants, 
        vote__name='Candidate C'
    ).count()

    for i, p in enumerate(participants):
        stats[f"p{i+1}_message_count"] = Message.objects.filter(group=group, sender=p).count()

    # Intervention counts
    stats['intervention_nudging'] = 0
    stats['intervention_summarization'] = 0
    stats['intervention_devils_advocate'] = 0
    
    intervention_counts = Counter(
        LlmMessage.objects.filter(group=group, is_intervention_analysis=False)
        .values_list('type_of_intervention', flat=True)
    )
    for intervention_type, count in intervention_counts.items():
        if intervention_type in ['nudging', 'summarization', 'devils_advocate']:
            stats[f"intervention_{intervention_type}"] = count

    # Survey and Record results
    turns = group.turns.all().order_by('turn_number')
    for i, p in enumerate(participants):
        prefix = f"p{i+1}_"
        
        # LLM Survey
        llm_survey = p.post_surveys_llm.first()
        if llm_survey:
            stats[f"{prefix}llm_summary"] = llm_survey.llm_summary
            stats[f"{prefix}llm_encouragement"] = llm_survey.llm_encouragement
            stats[f"{prefix}llm_alternatives"] = llm_survey.llm_alternatives
            stats[f"{prefix}llm_collaboration"] = llm_survey.llm_collaboration
            stats[f"{prefix}llm_satisfaction"] = llm_survey.llm_satisfaction
            stats[f"{prefix}llm_quality"] = llm_survey.llm_quality
            stats[f"{prefix}llm_recommendation"] = llm_survey.llm_recommendation
            stats[f"{prefix}llm_future_use"] = llm_survey.llm_future_use
        
        # Task Survey
        task_survey = p.post_surveys_task.first()
        if task_survey:
            stats[f"{prefix}dialogue_management"] = task_survey.dialogue_management
            stats[f"{prefix}information_pooling"] = task_survey.information_pooling
            stats[f"{prefix}reaching_consensus"] = task_survey.reaching_consensus
            stats[f"{prefix}time_management"] = task_survey.time_management
            stats[f"{prefix}reciprocal_interaction"] = task_survey.reciprocal_interaction
            stats[f"{prefix}individual_task_orientation"] = task_survey.individual_task_orientation

        # NASA Survey
        nasa_survey = p.post_surveys_task_nasa.first()
        if nasa_survey:
            stats[f"{prefix}mental_demand"] = nasa_survey.mental_demand
            stats[f"{prefix}temporal_demand"] = nasa_survey.temporal_demand
            stats[f"{prefix}performance"] = nasa_survey.performance
            stats[f"{prefix}effort"] = nasa_survey.effort
            stats[f"{prefix}frustration"] = nasa_survey.frustration
        
        # Initial and Formal Records per turn
        for turn in turns:
            turn_prefix = f"{prefix}turn{turn.turn_number}_"
            
            initial_record = InitialRecord.objects.filter(participant=p, turn=turn).select_related('vote').first()
            if initial_record and initial_record.vote:
                stats[f"{turn_prefix}initial_vote"] = initial_record.vote.name
            
            formal_record = FormalRecord.objects.filter(participant=p, turn=turn).select_related('vote').first()
            if formal_record and formal_record.vote:
                stats[f"{turn_prefix}formal_vote"] = formal_record.vote.name
            
    return stats

def build_open_responses_pdf(survey_responses, out_dir):
    """Builds a single PDF with all open-ended survey responses."""
    pdf_path = os.path.join(out_dir, "open_ended_responses.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    title_style = styles["Title"]
    header_style = ParagraphStyle("ResponseHeader", parent=styles["Normal"], fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6)
    content_style = styles["Normal"]

    story = [Paragraph("Open-Ended Survey Responses", title_style), Spacer(1, 24)]

    for survey in survey_responses:
        participant = survey.participant
        story.append(Paragraph(f"Group: {participant.group_id} | Participant: {participant._id}", header_style))
        story.append(Paragraph(survey.open_ended_response.replace("\n", "<br/>"), content_style))
        story.append(Spacer(1, 12))

    doc.build(story)
    print(f"\nOpen responses PDF saved -> {pdf_path}")

if __name__ == "__main__":
    base_dir = "new_setup" # <--- CHANGE THIS TO YOUR DESIRED OUTPUT FOLDER
    os.makedirs(base_dir, exist_ok=True)
    
    all_group_stats = []

    # Get all possible fieldnames for the CSV header
    fieldnames = set([
        'group_id', 'condition_id', 'condition_description', 'difficulty', 
        'initial_vote_A_count', 
        'formal_vote_A_count', 'formal_vote_B_count', 'formal_vote_C_count', 

        'total_messages', 
        'llm_messages_intervention', 
        'llm_messages_analysis_count',
        'intervention_nudging', 
        'intervention_summarization', 
        'intervention_devils_advocate','created_at'
    ])

    max_turns = Turn.objects.all().aggregate(Max('turn_number'))['turn_number__max'] or 0

    for i in range(1, 4): # Assuming max 3 participants
        fieldnames.add(f'p{i}_message_count')
        # Survey fields
        for survey_field in PostSurveyLLM._meta.get_fields():
            if not survey_field.is_relation and survey_field.name != '_id': fieldnames.add(f'p{i}_{survey_field.name}')
        for survey_field in PostSurveyTask._meta.get_fields():
            if not survey_field.is_relation and survey_field.name != '_id': fieldnames.add(f'p{i}_{survey_field.name}')
        for survey_field in PostSurveyNasa._meta.get_fields():
            if not survey_field.is_relation and survey_field.name != '_id': fieldnames.add(f'p{i}_{survey_field.name}')
        # Record fields
        for t in range(1, (max_turns or 0) + 1):
            fieldnames.add(f'p{i}_turn{t}_initial_vote')
            fieldnames.add(f'p{i}_turn{t}_formal_vote')

    sorted_fieldnames = sorted(list(fieldnames))

    for group in Group.objects.select_related('condition').all():
        # --- PDF Generation ---
        participants = group.participants.all()
        formal_records_count = FormalRecord.objects.filter(participant__in=participants).count()
        if formal_records_count < 3:
            print(f"Skipping Group {group._id}: Found only {formal_records_count} FormalRecords (Expected >= 3).")
            continue
            
        # Organize folders by condition and difficulty
        cond_id = group.condition._id
        difficulty = getattr(group, 'difficulty', 'N/A')
        
        group_dir = os.path.join(
            base_dir, 
            f"condition_{cond_id}", 
            f"difficulty_{difficulty}", 
            str(group._id)
        )
        os.makedirs(group_dir, exist_ok=True)
        
        print(f"Processing Group {group._id} (Condition {cond_id}, Difficulty {difficulty})...")
        for participant in group.participants.all():
            transcript = get_transcript_for_participant(participant)
            pdf_path = build_pdf_for_participant(group, participant, transcript, group_dir)
            print(f"  PDF saved -> {pdf_path}")
            
        # --- CSV Data Aggregation ---
        stats = get_group_stats(group)
        all_group_stats.append(stats)

    # --- Write CSV File ---
    csv_path = os.path.join(base_dir, "group_summary.csv")
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted_fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(all_group_stats)
        print(f"\nSuccessfully created summary CSV -> {csv_path}")
    except IOError as e:
        print(f"\nError writing CSV file: {e}")

    # --- Build Open-Ended Responses PDF ---
    open_ended_surveys = PostSurveyLLM.objects.filter(open_ended_response__isnull=False).exclude(open_ended_response='').select_related('participant')
    if open_ended_surveys.exists():
        build_open_responses_pdf(open_ended_surveys, base_dir)