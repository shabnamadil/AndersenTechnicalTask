import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify as custom_slugify

from apps.tasks.models import Task

User = get_user_model()


@receiver(post_save, sender=Task)
def set_task_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        instance.slug = custom_slugify(f'{instance.title}-{instance.id}')
        instance.save(update_fields=['slug']) 
