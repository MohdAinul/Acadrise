# Generated by Django 5.1.2 on 2024-11-28 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_studentverification_profile_email_verified_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='class_levels',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_teacher',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pin_code',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='subjects',
        ),
    ]
