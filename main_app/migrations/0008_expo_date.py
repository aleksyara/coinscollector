# Generated by Django 3.1.4 on 2020-12-14 01:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20201213_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='expo',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
