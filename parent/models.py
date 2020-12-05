from django.db import models

# Create your models here.

class Events(models.Model) :
    title = models.CharField(max_length=100) 
    description = models.TextField()
    date = models.DateTimeField()
    
    class Meta:
        ordering = ["-date"]

class Holidays(models.Model) :
    title = models.CharField(max_length=100) 
    date = models.DateField()
    class Meta:
        ordering = ["-date"]



