# Generated by Django 2.2 on 2020-05-14 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20200514_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]