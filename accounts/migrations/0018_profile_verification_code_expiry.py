# Generated by Django 5.1.2 on 2024-12-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_profile_otp_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verification_code_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]