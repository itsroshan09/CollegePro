# Generated by Django 4.0.3 on 2024-06-07 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allstaffdatabase', '0003_allstaffdatabase_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allstaffdatabase',
            old_name='contact',
            new_name='selfcontact',
        ),
    ]