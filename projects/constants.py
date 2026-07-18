from django.db import models


class ProjectStatus(models.TextChoices):
    NOT_STARTED = "not_started", "Not Started"
    IN_PROGRESS = "in_progress", "In Progress"
    ON_HOLD = "on_hold", "On Hold"
    COMPLETED = "completed", "Completed"


class JobStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", "In Progress"
    ON_HOLD = "on_hold", "On Hold"
    ASSESSMENT_COMPLETED = "assessment_completed", "Assessment Completed"
    SITE_VISIT_COMPLETED = "site_visit_completed", "Site Visit Completed"


class TemplateType(models.TextChoices):
    PRE_INSTALLATION = "pre_installation", "Pre Installation"
    POST_INSTALLATION = "post_installation", "Post Installation"


class JobParameterKey(models.TextChoices):
    PITCH = "pitch", "Pitch"
    OBSTRUCTIONS = "obstructions", "Obstructions"