# Generated by Django 2.2 on 2020-05-14 21:30

import core.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20200515_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date_time',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AddField(
            model_name='question',
            name='deadline',
            field=models.DateField(default=core.models.get_deadline),
        ),
    ]