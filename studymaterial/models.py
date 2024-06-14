from django.db import models

# Create your models here.
class studymaterial(models.Model):
    DEPARTMENT_CHOICES = [
        ('Artificial Intelligence Department', 'Artificial Intelligence Department'),
        ('Information Technology Department', 'Information Technology Department'),
        ('Computer Engineering Department', 'Computer Engineering Department'),
        ('Mechanical Department', 'Mechanical Engineering Department'),
        ('Electrical Department', 'Electrical Engineering Department'),
        ('Civil Department', 'Civil Engineering Department'),
    ]

    department = models.CharField(max_length=200, choices=DEPARTMENT_CHOICES)
    file=models.FileField(upload_to="uploads/",max_length=1000,null=True)
    filename=models.TextField(max_length=500)