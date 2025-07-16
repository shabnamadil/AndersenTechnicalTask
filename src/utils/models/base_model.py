from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def created_date(self):
        local_created_time = timezone.localtime(self.created_at)
        return local_created_time.strftime("%d %b %Y, %H:%M")

    @property
    def updated_date(self):
        local_updated_time = timezone.localtime(self.updated_at)
        return local_updated_time.strftime("%d/%m/%Y, %H:%M")
