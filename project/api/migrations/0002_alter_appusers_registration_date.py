# Generated by Django 5.1.5 on 2025-02-11 11:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appusers',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 11, 11, 30, 34, 796510, tzinfo=datetime.timezone.utc)),
        ),
    ]
