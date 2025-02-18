# Generated by Django 5.1.5 on 2025-02-11 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_appusers_registration_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstracks',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='userstracks',
            name='cover_url',
        ),
        migrations.RemoveField(
            model_name='userstracks',
            name='lyrics',
        ),
        migrations.RemoveField(
            model_name='userstracks',
            name='track_title',
        ),
        migrations.AlterField(
            model_name='appusers',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 11, 11, 35, 49, 810081, tzinfo=datetime.timezone.utc)),
        ),
    ]
