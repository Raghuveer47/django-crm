# Generated by Django 5.0.6 on 2024-06-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='sequential_number',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]