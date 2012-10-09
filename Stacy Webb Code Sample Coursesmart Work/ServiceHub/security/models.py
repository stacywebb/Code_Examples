
from django.db import models

class UserIdentity(models.Model):
    userId = models.SlugField(max_length=24)
    isCurrentUser = models.BooleanField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    emailAddress = models.EmailField(max_length=75)
    role = models.CharField(max_length=16)
     
    def __str__(self):
        result = ''
        if self.isCurrentUser:
            result = '*'
        result += self.userId
        return result
    
