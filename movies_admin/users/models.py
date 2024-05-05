from http import HTTPStatus
import json
import uuid
from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import requests


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="auth_profile")
    uuid = models.UUIDField(unique=True, null=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self) -> str:
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.auth_profile.save()


class UserPermission(UUIDMixin):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    resource = models.CharField(max_length=150)

    class Meta:
        verbose_name = _("permission")
        verbose_name_plural = _("permissions")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        url = settings.AUTH_API_PERMISSION
        payload = {
            'name': self.name,
            'description': self.description,
            'resource': self.resource
        }
        from_api = requests.get(f"{url}/{self.id}")
        if from_api.status_code == HTTPStatus.OK:
            response = requests.patch(f"{url}/{self.id}", data=json.dumps(payload))
            if response.status_code != HTTPStatus.OK:
                return None
        if from_api.status_code == HTTPStatus.NOT_FOUND:
            response = requests.post(url, data=json.dumps(payload))
            if response.status_code != HTTPStatus.CREATED:
                return None
        data = response.json()
        self.id = data.get('id')
        return super(UserPermission, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        url = settings.AUTH_API_PERMISSION
        response = requests.delete(f"{url}/{self.id}")
        if response.status_code == HTTPStatus.NO_CONTENT:
            return super(UserPermission, self).delete(*args, **kwargs)



class UserRole(UUIDMixin):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = _("user_role")
        verbose_name_plural = _("user_roles")

class UserRolePermissions(UUIDMixin):
    role = models.ForeignKey("UserPermission", on_delete=models.CASCADE)
    permission = models.ForeignKey("UserRole", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role} ({self.permission})"
