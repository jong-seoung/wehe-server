from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Skill(models.Model):
    name = models.CharField(_("skill"), max_length=30, blank=True, null=True)

    def skill_image_path(instance, filename):
        return os.path.join("skill_images", f"{instance.name}_img.webp")

    image = models.ImageField(
        _("skill image"),
        upload_to=skill_image_path,
        blank=True,
        storage=OverwriteStorage(),
    )

    def __str__(self):
        return self.name