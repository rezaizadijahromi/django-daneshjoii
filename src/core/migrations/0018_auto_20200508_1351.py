# Generated by Django 3.0.5 on 2020-05-08 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200508_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='question_req',
            field=models.ManyToManyField(related_name='user', to='core.Question'),
        ),
    ]