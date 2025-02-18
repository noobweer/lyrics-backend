# Generated by Django 5.1.5 on 2025-02-11 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_userstracks_artist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstracks',
            name='artist',
            field=models.CharField(default='default_artist', max_length=255),
        ),
        migrations.AddField(
            model_name='userstracks',
            name='cover_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userstracks',
            name='lyrics',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userstracks',
            name='track_title',
            field=models.CharField(default='default_title', max_length=255),
        ),
        migrations.AlterField(
            model_name='appusers',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 11, 11, 37, 57, 566275, tzinfo=datetime.timezone.utc)),
        ),
    ]
