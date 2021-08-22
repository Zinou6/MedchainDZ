# Generated by Django 3.2.4 on 2021-08-19 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0057_auto_20210818_0105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='boite10',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='boite6',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='boite7',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='boite8',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='boite9',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='doc',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicament10',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicament6',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicament7',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicament8',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medicament9',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='traitement10',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='traitement6',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='traitement7',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='traitement8',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='traitement9',
        ),
        migrations.AddField(
            model_name='prescription',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='prescription',
            name='doctorId',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patientId',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
