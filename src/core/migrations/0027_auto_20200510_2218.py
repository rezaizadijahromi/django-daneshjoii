# Generated by Django 2.2 on 2020-05-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_answer_answered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.ManyToManyField(related_name='answer', to='core.Answer'),
        ),
    ]