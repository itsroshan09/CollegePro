# Generated by Django 4.0.3 on 2024-06-05 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studymaterial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studymaterial',
            name='department',
            field=models.CharField(choices=[('AI', 'Artificial Intelligence Department'), ('IT', 'Information Technology Department'), ('CE', 'Computer Engineering Department'), ('ME', 'Mechanical Department'), ('EE', 'Electrical Department'), ('CV', 'Civil Department')], max_length=2),
        ),
    ]