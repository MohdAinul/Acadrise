# Generated by Django 5.1.2 on 2024-11-09 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_chatmessage_connectionrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionrequest',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
