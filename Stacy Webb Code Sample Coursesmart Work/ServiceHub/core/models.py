__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'

from django.db import models
from datetime import datetime

class Tenant(models.Model):
    tenantKey = models.SlugField(max_length=16)
    tenantName = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=20)
    stateId = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    contactEmail = models.EmailField(blank=True)
    contactPhone = models.CharField(max_length=24, blank=True)
    csUrlPrefix = models.CharField(max_length=128)
    portal = models.SlugField(max_length=8)
    portalId = models.PositiveIntegerField(max_length=4)
    redemptionFormat = models.PositiveIntegerField(max_length=1)
    
    def __str__(self):
        return self.tenantKey
    
class Imprint(models.Model):
    imprintKey = models.SlugField(max_length=64)
    imprint = models.CharField(max_length=64)
    publisher = models.CharField(max_length=64)
    
    def __str__(self):
        return self.imprint
        
class EResource(models.Model):
    fpId = models.SlugField(max_length=15)
    imprint = models.ForeignKey(Imprint, null=True)
    
    def __str__(self):
        return self.fpid
    
class SiteUser(models.Model):
    tenant = models.ForeignKey(Tenant)
    userId = models.SlugField(max_length=24)
    role = models.SlugField(max_length=16)
    csUserId = models.CharField(max_length=8)
    csAccountId = models.CharField(max_length=8)
    
    def __str__(self):
        return self.userId

class Course(models.Model):
    courseId = models.SlugField()
    
    def __str__(self):
        return self.courseId
    
class CourseRequirement(models.Model):
    course = models.ForeignKey(Course)
    isbn = models.SlugField()
    title = models.CharField(max_length=48)
    author = models.CharField(max_length=24)
    
    def __str__(self):
        return self.course.courseId + ": " + self.isbn
