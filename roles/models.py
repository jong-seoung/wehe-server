from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(_("Role"), max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
