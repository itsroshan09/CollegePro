from django.db import models

# Create your models here.

class courses(models.Model):
    icon=models.FileField(upload_to="uploads/",null=True,default=None,max_length=250)
    detail=models.TextField(max_length=10000)