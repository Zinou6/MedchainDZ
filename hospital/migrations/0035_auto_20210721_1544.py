# Generated by Django 3.2.4 on 2021-07-21 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0034_rename_profile_doctor_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='user',
        ),
        migrations.AddField(
            model_name='doctor',
            name='profile',
            field=models.OneToOneField(default=False, on_delete=django.db.models.deletion.CASCADE, to='hospital.profile'),
        ),
    ]
