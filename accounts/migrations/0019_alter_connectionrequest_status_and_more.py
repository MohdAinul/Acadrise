# Generated by Django 5.1.2 on 2024-12-15 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_profile_verification_code_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], max_length=10),
        ),
    ]