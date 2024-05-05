
from django.db import models

# Create your models here.
class Task(models.Model):
    Name = models.CharField(max_length = 50)
    password = models.IntegerField(max_length = 10)
   

  

