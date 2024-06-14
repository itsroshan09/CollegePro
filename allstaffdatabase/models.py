from django.db import models

class allstaffdatabase(models.Model):
    DEPARTMENT_CHOICES = [
        ('Principal', "Principal"),
        ('Artificial Intelligence Department', 'Artificial Intelligence Department'),
        ('Information Technology Department', 'Information Technology Department'),
        ('Computer Engineering Department', 'Computer Engineering Department'),
        ('Mechanical Engineering Department', 'Mechanical Engineering Department'),
        ('Electrical Engineering Department', 'Electrical Engineering Department'),
        ('Civil Engineering Department', 'Civil Engineering Department'),
    ]
    photo = models.ImageField(upload_to="uploads/", max_length=1000, null=True)
    name = models.CharField(max_length=2000)
    designation = models.CharField(max_length=2000, default=None)
    department = models.CharField(max_length=200, choices=DEPARTMENT_CHOICES, default=None, null=True)
    aadhar_no = models.CharField(max_length=20)
    addressline = models.TextField(max_length=2000)
    contact = models.CharField(max_length=10, null=True, unique=True)

    def __str__(self):
        return self.name
