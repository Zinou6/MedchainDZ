# Generated by Django 3.2.4 on 2021-07-07 14:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0024_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='symptoms',
        ),
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='patient',
            name='brth_day',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='patient',
            name='nom_jeune_fille',
            field=models.CharField(default='NA', max_length=40),
        ),
        migrations.AddField(
            model_name='patient',
            name='sexe',
            field=models.CharField(choices=[('Man', 'Man'), ('Woman', 'Woman')], default='Man', max_length=20),
        ),
        migrations.AddField(
            model_name='patient',
            name='situation_F',
            field=models.CharField(default='single', max_length=40),
        ),
        migrations.DeleteModel(
            name='profile',
        ),
    ]
