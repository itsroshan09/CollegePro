from django.db import models
from datetime import datetime


YEAR_CHOICES=[]
def year_choices():
    for i in range(2000,datetime.now().year + 2):
        tp=(str(i),str(i))
        YEAR_CHOICES.append(tp)
    return YEAR_CHOICES

class marksheetdata(models.Model):
    name = models.CharField(max_length=200)
    enrollment = models.CharField(max_length=20)
    DEPARTMENT_CHOICES = [
        ('Artificial Intelligence Department', 'Artificial Intelligence Department'),
        ('Information Technology Department', 'Information Technology Department'),
        ('Computer Engineering Department', 'Computer Engineering Department'),
        ('Mechanical Department', 'Mechanical Department'),
        ('Electrical Department', 'Electrical Department'),
        ('Civil Department', 'Civil Department'),
    ]

    

    department = models.CharField(max_length=200, choices=DEPARTMENT_CHOICES)
    result = models.TextField()
    total_marks = models.PositiveBigIntegerField()
    total_marks_obtained = models.PositiveBigIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('year').choices = year_choices()

    year = models.CharField(choices=year_choices(), default=datetime.now().year, max_length=5)
