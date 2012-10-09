
from django.db import models

class RedemptionProgram(models.Model):
    publisherCode = models.CharField(max_length=64)
    redemptionProgram = models.PositiveIntegerField()