
from django.db import models
from core.models import Tenant

class RedirectorTemplate(models.Model):
    templateName = models.SlugField(max_length=24)
    template = models.CharField(max_length=256)

    def __str__(self):
        return self.templateName