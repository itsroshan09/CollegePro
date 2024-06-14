from django.db import models

# Create your models here.
class staffusers(models.Model):
    username=models.CharField(max_length=250,default=None,null=False,unique=True)
    password=models.CharField(max_length=1000,default=None,null=False,unique=False)