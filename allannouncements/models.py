from django.db import models
from django.utils import timezone

class allannouncements(models.Model):
    ANNOUNCEMENT_CATEGORIES = [
        ('General', 'General'),
        ('Event', 'Event'),
        ('Update', 'Update'),
        ('Alert', 'Alert'),
    ]
    category = models.CharField(max_length=50, choices=ANNOUNCEMENT_CATEGORIES, default='General')
    announcement = models.TextField(max_length=3000)
    date = models.DateField(default=timezone.now, null=False)

    
