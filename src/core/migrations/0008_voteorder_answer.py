# Generated by Django 2.2 on 2020-05-25 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200522_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteorder',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Answer'),
        ),
    ]
