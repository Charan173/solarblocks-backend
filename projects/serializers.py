from rest_framework import serializers

from projects.constants import JobStatus
from .models import JobParameter, Project


class JobParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobParameter
        fields = ['id', 'key', 'notes', 'photo', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class ProjectListSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'category', 'address', 'status', 'assigned_to_name','template_type']

    def get_assigned_to_name(self, obj):
        return obj.assigned_to.get_full_name() or obj.assigned_to.username if obj.assigned_to else None


class ProjectDetailSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.SerializerMethodField()
    parameters = JobParameterSerializer(many=True, read_only=True)
    
    def get_assigned_to_name(self, obj):
        return obj.assigned_to.get_full_name() or obj.assigned_to.username if obj.assigned_to else None

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'category', 'address', 'status', 'job_status','template_type', 'assigned_to_name', 'parameters', 'created_at',
        ]



class ProjectStatusUpdateSerializer(serializers.Serializer):
    job_status = serializers.ChoiceField(choices=JobStatus.choices)