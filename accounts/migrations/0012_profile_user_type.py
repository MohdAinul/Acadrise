# Generated by Django 5.1.2 on 2024-11-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_profile_class_levels_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('student', 'Student'), ('teacher', 'Teacher')], max_length=10, null=True),
        ),
    ]
