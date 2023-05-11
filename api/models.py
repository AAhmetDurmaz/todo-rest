from django.db import models
from uuid import uuid4 as uuid
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid)
    list_id = models.UUIDField(null=False)
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    completed = models.BooleanField(default=False, blank=False)
    creator = models.UUIDField(default=None, null=True)

    objects = models.Manager()
    def soft_delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
        super(Task, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.creator:
            self.creator = kwargs.get('creator')
        super(Task, self).save(*args, **kwargs)


class TaskList(models.Model, ):
    id = models.UUIDField(primary_key=True, default=uuid)
    name = models.CharField(max_length=255)
    completion_percentage = models.PositiveIntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    creator = models.UUIDField(default=None, null=True)

    objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.creator:
            self.creator = kwargs.get('creator')
        super(TaskList, self).save(*args, **kwargs)
