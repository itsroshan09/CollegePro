# Generated by Django 4.0.3 on 2024-06-12 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='staffusers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=250, unique=True)),
                ('password', models.CharField(default=None, max_length=1000)),
            ],
        ),
    ]
