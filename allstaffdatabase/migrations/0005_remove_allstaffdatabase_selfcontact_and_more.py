# Generated by Django 4.0.3 on 2024-06-07 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allstaffdatabase', '0004_rename_contact_allstaffdatabase_selfcontact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allstaffdatabase',
            name='selfcontact',
        ),
        migrations.AddField(
            model_name='allstaffdatabase',
            name='selfc',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
