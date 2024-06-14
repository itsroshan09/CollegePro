from django.db import models

# Create your models here.
class reviews(models.Model):
    RATING_CHOICES=[(5,5),(4,4),(3,3),(2,2),(1,1)]
    photo=models.ImageField(upload_to="uploads/",max_length=250,null=False,default=None)
    name=models.CharField(max_length=200)
    rating=models.IntegerField(choices=RATING_CHOICES,null=False,default=5)
    review=models.TextField(max_length=2000,default=None)