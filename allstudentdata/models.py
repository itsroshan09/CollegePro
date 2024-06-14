from django.db import models

# Create your models here.
class allstudentdata(models.Model):
    photo=models.ImageField(upload_to="uploads/",max_length=2000,null=True)
    name=models.CharField(max_length=3000)
    enrollment=models.CharField(max_length=3000)
    DEPARTMENT_CHOICES = [
        
        ('Artificial Intelligence Department', 'Artificial Intelligence Department'),
        ('Information Technology Department', 'Information Technology Department'),
        ('Computer Engineering Department', 'Computer Engineering Department'),
        ('Mechanical Engineering Department', 'Mechanical Engineering Department'),
        ('Electrical Engineering Department', 'Electrical Engineering Department'),
        ('Civil Engineering Department', 'Civil Engineering Department'),
    ]
    department = models.CharField(max_length=500, choices=DEPARTMENT_CHOICES,default=None,null=True)
    dob=models.DateField()
    cast=models.CharField(max_length=200)
    selfcontact=models.CharField(max_length=10)
    parentcontact=models.CharField(max_length=10)
    aadhar=models.CharField(max_length=20)
    address=models.TextField(max_length=3000)
