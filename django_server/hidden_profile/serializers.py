from rest_framework import serializers
from .models import CandidateProfile

class CandidateProfileSerializer(serializers.ModelSerializer):
    uuid_field = serializers.UUIDField(format='hex', source='_id')
    
    class Meta:
        model = CandidateProfile
        fields = '__all__'
    
    
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        role = self.context.get("role")
        
        if role is None:
            raise ValueError("Role cannot be None")
        
        allowed_fields = [
            '_id',
            'name',
            'number_of_courses_taught',
            'student_teaching_evaluations',
            'number_of_peer_reviewed_publications',
            'citations',
            'service_on_editorial_boards',
            'conference_organization_roles',
        ]
        
        if role == 1:
            allowed_fields.extend([
                'undergraduate_mentorship_success',
                'graduate_thesis_supervision',
                'curriculum_development',
                'teaching_awards',
            ])
        elif role == 2:
            allowed_fields.extend([
                'grant_funding_secured',
                'reviewer_activity',
                'interdisciplinary_research',
                'research_awards',
            ])
        elif role == 3:
            allowed_fields.extend([
                'invited_talks',
                'industry_collaboration',
                'university_committee_service',
                'research_coverage',
            ])
            
        return {key: value for key, value in representation.items() if key in allowed_fields}