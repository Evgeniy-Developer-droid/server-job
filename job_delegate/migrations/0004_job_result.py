# Generated by Django 4.0.1 on 2022-01-11 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_delegate', '0003_rename_clientdata_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='result',
            field=models.TextField(default='{}'),
        ),
    ]
