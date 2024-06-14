from django.db import models

# Create your models here.
class slideshow(models.Model):
    file=models.FileField(max_length=1000,null=True,default=None)