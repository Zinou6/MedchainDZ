# Generated by Django 3.2.4 on 2021-08-18 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0056_document_prescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='assignedDoctorName',
        ),
        migrations.RemoveField(
            model_name='document',
            name='patientName',
        ),
        migrations.AddField(
            model_name='document',
            name='doctorId',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
