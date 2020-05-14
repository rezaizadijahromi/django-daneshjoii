# Generated by Django 3.0.5 on 2020-05-06 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200507_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='poity',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_answer', models.ImageField(upload_to='answer/')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
