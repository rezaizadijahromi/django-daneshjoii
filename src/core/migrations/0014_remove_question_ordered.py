# Generated by Django 3.0.5 on 2020-05-07 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200508_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='ordered',
        ),
    ]