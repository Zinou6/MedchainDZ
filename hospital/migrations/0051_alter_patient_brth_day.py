# Generated by Django 3.2.4 on 2021-08-09 04:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0050_patient_brth_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='brth_day',
            field=models.CharField(default=datetime.date.today, max_length=40),
        ),
    ]
