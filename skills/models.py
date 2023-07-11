from django.db import models
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    name = models.CharField(_("skill"), max_length=30, blank=True, null=True)
    image = models.ImageField(_("skill image"), upload_to="skill_images/", blank=True)
