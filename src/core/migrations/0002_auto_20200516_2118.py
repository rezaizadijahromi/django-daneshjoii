# Generated by Django 2.2 on 2020-05-16 16:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='question',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]
