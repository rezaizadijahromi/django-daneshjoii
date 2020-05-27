# Generated by Django 2.2 on 2020-05-27 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200527_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='likes',
        ),
        migrations.AlterField(
            model_name='dislike',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Answer'),
        ),
        migrations.AlterField(
            model_name='like',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Answer'),
        ),
    ]