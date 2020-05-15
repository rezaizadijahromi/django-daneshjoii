# Generated by Django 3.0.5 on 2020-05-08 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_order_ordered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='question_req',
        ),
        migrations.AddField(
            model_name='order',
            name='question_req',
            field=models.ManyToManyField(to='core.Question'),
        ),
    ]