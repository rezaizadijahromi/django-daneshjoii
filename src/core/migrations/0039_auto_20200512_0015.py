# Generated by Django 2.2 on 2020-05-11 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_answerquantity_voteorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerquantity',
            name='ordered',
        ),
        migrations.AddField(
            model_name='answerquantity',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Answer'),
        ),
        migrations.AlterField(
            model_name='answerquantity',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
