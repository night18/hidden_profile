# filepath: hidden_profile/management/commands/create_candidates.py
from django.core.management.base import BaseCommand
from hidden_profile.models import CandidateProfile

class Command(BaseCommand):
    help = 'Creates the initial set of candidate profiles for both difficulties.'

    def handle(self, *args, **options):
        self.stdout.write('Starting to create/update candidate profiles...')

        # --- Candidate Data ---
        # You can define all your candidates here
        candidates_data = [
            # Difficulty / Pair 1


        {
            "pair": 0, "difficult": 0, "name": "Candidate A", "winner": True,

            #"number_of_courses_taught": "Average",
            #"student_teaching_evaluations": "Good",
            "number_of_peer_reviewed_publications": "Exceptional",
            "citations": "Average",
            "service_on_editorial_boards": "Good",
            "conference_organization_roles": "Good",

            "undergraduate_mentorship_success": "Exceptional",
            #"graduate_thesis_supervision": "Exceptional",
            #"curriculum_development": "Exceptional",
            "teaching_awards": "Exceptional",

            "grant_funding_secured": "Exceptional",
            #"reviewer_activity": "Exceptional",
            "interdisciplinary_research": "Good",
            #"research_awards": "Good",

            #"invited_talks": "Good",
            "industry_collaboration": "Exceptional",
            #"university_committee_service": "Exceptional",
            "research_coverage": "Good"
        },
        {
            "pair": 0, "difficult": 0, "name": "Candidate B", "winner": False,


            #"number_of_courses_taught": "Average",
            #"student_teaching_evaluations": "Good",
            "number_of_peer_reviewed_publications": "Average",
            "citations": "Exceptional",
            "service_on_editorial_boards": "Good",
            "conference_organization_roles": "Exceptional",

            "undergraduate_mentorship_success": "Good",
            #"graduate_thesis_supervision": "Exceptional",
            #"curriculum_development": "Exceptional",
            "teaching_awards": "Good",

            "grant_funding_secured": "Average",
            #"reviewer_activity": "Exceptional",
            "interdisciplinary_research": "Exceptional",
            #"research_awards": "Good",

            #"invited_talks": "Good",
            "industry_collaboration": "Good",
            #"university_committee_service": "Exceptional",
            "research_coverage": "Exceptional"
        },
        {
            "pair": 0, "difficult": 0, "name": "Candidate C", "winner": False,


            #"number_of_courses_taught": "Average",
            #"student_teaching_evaluations": "Good",
            "number_of_peer_reviewed_publications": "Good",
            "citations": "Good",
            "service_on_editorial_boards": "Exceptional",
            "conference_organization_roles": "Good",

            "undergraduate_mentorship_success": "Good",
            #"graduate_thesis_supervision": "Exceptional",
            #"curriculum_development": "Exceptional",
            "teaching_awards": "Good",

            "grant_funding_secured": "Average",
            #"reviewer_activity": "x",
            "interdisciplinary_research": "Good",
            #"research_awards": "Good",

            #"invited_talks": "Good",
            "industry_collaboration": "Good",
            #"university_committee_service": "Exceptional",
            "research_coverage": "Average"
        }
        ,
{
  "pair": 0,
  "difficult": 1,
  "name": "Candidate A",
  "winner": true,

  "publications": "Average",
  "citations": "Good",
  "service": "Good",
  "conference_organization": "Good",

  "mentorship": "Exceptional",
  "teaching": "Exceptional",

  "funding": "Exceptional",
  "interdisciplinarity": "Exceptional",

  "colaborations": "Exceptional",
  "research_coverage": "Exceptional"
},
{
  "pair": 0,
  "difficult": 1,
  "name": "Candidate B",
  "winner": false,

  "publications": "Exceptional",
  "citations": "Exceptional",
  "service": "Exceptional",
  "conference_organization": "Exceptional",

  "mentorship": "Average",
  "teaching": "Good",

  "funding": "Average",
  "interdisciplinarity": "Good",

  "colaborations": "Good",
  "research_coverage": "Good"
},
{
  "pair": 0,
  "difficult": 1,
  "name": "Candidate C",
  "winner": false,

  "publications": "Average",
  "citations": "Good",
  "service": "Good",
  "conference_organization": "Good",

  "mentorship": "Average",
  "teaching": "Good",

  "funding": "Average",
  "interdisciplinarity": "Good",

  "colaborations": "Good",
  "research_coverage": "Average"
},

  {
    "pair": 0,
    "difficult": 2,
    "name": "Candidate A",
    "winner": True,

            #"number_of_courses_taught": "Average",
            #"student_teaching_evaluations": "Good",
            "publications": "Good",
            "citations": "Exceptional",
            "service": "Average",
            "conference_organization": "Good",

            "mentorship": "Exceptional",
            #"graduate_thesis_supervision": "Exceptional",
            #"curriculum_development": "Exceptional",
            "teaching": "Exceptional",

            "funding": "Good",
            #"reviewer_activity": "Exceptional",
            "interdisciplinarity": "Good",
            #"research_awards": "Good",

            #"invited_talks": "Good",
            "colaborations": "Good",
            #"university_committee_service": "Exceptional",
            "research_coverage": "Exceptional"
  },
  {
    "pair": 0,
    "difficult": 2,
    "name": "Candidate B",
    "winner": False,

            #"number_of_courses_taught": "Average",
            #"student_teaching_evaluations": "Good",
            "publications": "Exceptional",
            "citations": "Good",
            "service": "Average",
            "conference_organization": "Good",

            "mentorship": "Average",
            #"graduate_thesis_supervision": "Exceptional",
            #"curriculum_development": "Exceptional",
            "teaching": "Good",

            "funding": "Exceptional",
            #"reviewer_activity": "Exceptional",
            "interdisciplinarity": "Exceptional",
            #"research_awards": "Good",

            #"invited_talks": "Good",
            "colaborations": "Good",
            #"university_committee_service": "Exceptional",
            "research_coverage": "Average"
  },
  {
    "pair": 0,
    "difficult": 2,
    "name": "Candidate C",
    "winner": False,

            #"number_of_courses_taught": "Average",
            #"student_teaching_evaluations": "Good",
            "publications": "Average",
            "citations": "Good",
            "service": "Exceptional",
            "conference_organization": "Exceptional",

            "mentorship": "Average",
            #"graduate_thesis_supervision": "Exceptional",
            #"curriculum_development": "Exceptional",
            "teaching": "Good",

            "funding": "Average",
            #"reviewer_activity": "Exceptional",
            "interdisciplinarity": "Good",
            #"research_awards": "Good",

            #"invited_talks": "Good",
            "colaborations": "Exceptional",
            #"university_committee_service": "Exceptional",
            "research_coverage": "Average"
  }



        ]

        for data in candidates_data:
            # Use get_or_create to avoid duplicates.
            # It looks for an object with the specified fields (name, pair).
            # If it exists, it does nothing. If not, it creates it with the 'defaults'.
            name = data.pop("name")
            difficult = data.pop("difficult")
            
            obj, created = CandidateProfile.objects.update_or_create(
                name=name,
                difficult=difficult,
                defaults=data
            )


            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created Candidate {name} for difficulty {difficult}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated Candidate {name} for difficulty {difficult}'))
