# Generated by Django 2.2 on 2020-07-17 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_new_v', '0002_auto_20200717_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ref_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
