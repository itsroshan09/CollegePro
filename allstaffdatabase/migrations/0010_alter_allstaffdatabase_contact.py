# Generated by Django 4.0.3 on 2024-06-07 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allstaffdatabase', '0009_rename_self contact_allstaffdatabase_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allstaffdatabase',
            name='contact',
            field=models.CharField(default='123', max_length=10, null=True, unique=True),
        ),
    ]
