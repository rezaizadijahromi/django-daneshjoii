# Generated by Django 2.2 on 2020-07-17 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_question_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='quentity',
            field=models.IntegerField(default=0),
        ),
    ]
