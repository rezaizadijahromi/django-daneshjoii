# Generated by Django 2.2 on 2020-05-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200522_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
