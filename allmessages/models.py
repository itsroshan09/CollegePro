from django.db import models

# Create your models here.
class allmessages(models.Model):
        name=models.CharField(max_length=2000)
        email=models.EmailField(max_length=200)
        message=models.TextField()
        read=models.BooleanField(default=False)