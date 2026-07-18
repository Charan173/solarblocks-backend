from django.conf import settings
from django.db import models
from django_softdelete.models import SoftDeleteModel

from .constants import (
    JobParameterKey,
    JobStatus,
    ProjectStatus,
    TemplateType,
)


class Project(SoftDeleteModel, models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.NOT_STARTED,
    )

    job_status = models.CharField(
        max_length=30,
        choices=JobStatus.choices,
        blank=True,
    )

    template_type = models.CharField(
        max_length=30,
        choices=TemplateType.choices,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class JobParameter(SoftDeleteModel, models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="parameters",
    )

    key = models.CharField(
        max_length=30,
        choices=JobParameterKey.choices,
    )

    notes = models.TextField(blank=True)

    photo = models.ImageField(
        upload_to="job_parameters/",
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "key")

    def __str__(self):
        return f"{self.project.name} - {self.get_key_display()}"