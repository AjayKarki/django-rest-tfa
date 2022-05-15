import uuid
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
    )
    is_active = models.BooleanField(default=True)
    is_obsolete = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @classmethod
    def new(cls, **kwargs):
            return cls.objects.create(**kwargs)

    def delete(self):
        self.is_obsolete = True
        self.deleted_at = timezone.now()
        super().save(update_fields=['is_obsolete', 'deleted_at'])
