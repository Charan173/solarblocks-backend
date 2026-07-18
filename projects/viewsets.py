from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from solarblocks import authentication

from .models import JobParameter, Project, JobParameterKey


from .serializers import (
    JobParameterSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProjectStatusUpdateSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    /api/projects/                         -> list, create
    /api/projects/{pk}/                    -> retrieve, update, partial_update, destroy
    /api/projects/{pk}/status/     [PATCH] -> update_status  (custom action)
    /api/projects/{pk}/parameters/{key}/   -> parameter       (custom action, GET + PATCH)
    """
    queryset = Project.objects.all().order_by('-created_at')
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    )
    # throttle_scope = 'request'
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        template_type = self.request.query_params.get('template_type')
        if search:
            qs = qs.filter(name__icontains=search)
        if status_filter and status_filter != 'All':
            qs = qs.filter(status=status_filter)
            
        if template_type and template_type != 'All':
            qs = qs.filter(template_type=template_type)
        
        return qs

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project.job_status = serializer.validated_data['job_status']
        project.save(update_fields=['job_status'])
        return Response(ProjectDetailSerializer(project).data)

    @action(
        detail=True,
        methods=['get', 'patch'],
        url_path=r'parameters/(?P<key>[^/.]+)',
        parser_classes=[MultiPartParser, FormParser,JSONParser],
    )
    def parameter(self, request, pk=None, key=None):
        project = self.get_object()
        if key not in JobParameterKey.values:
            return Response(
                {"detail": "Invalid parameter key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj, _ = JobParameter.objects.get_or_create(project=project, key=key)

        if request.method == 'GET':
            return Response(JobParameterSerializer(obj).data)

        serializer = JobParameterSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)